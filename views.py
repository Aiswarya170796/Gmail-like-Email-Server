from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Email, Recipient ,Attachment
from django.contrib.auth.models import User
from django.db.models import Q
import json

def home(request):
    print("Executing home view")
    return render(request, 'home.html')

def register(request):
    print("Executing register view")
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        print(f"Received data: username={username}, email={email}, password={password}, confirm_password={confirm_password}")

        if username and email and password and confirm_password:
            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                print("Passwords do not match.")
            else:
                try:
                    if User.objects.filter(username=username).exists():
                        messages.error(request, 'Username already exists.')
                        print("Username already exists.")
                    else:
                        user = User.objects.create_user(username=username, email=email, password=password)
                        login(request, user)
                        print("User registered and logged in successfully.")
                        return redirect('dashboard')
                except Exception as e:
                    messages.error(request, f'Error during registration: {e}')
                    print(f'Error during registration: {e}')
        else:
            messages.error(request, 'All fields are required.')
            print("All fields are required.")

    return render(request, 'register.html')

def user_login(request):
    print("Executing user_login view")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Received login attempt: username={username}, password={password}")

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    print("User logged in successfully.")
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Your account is inactive.')
                    print("User account is inactive.")
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
                print("Invalid username or password.")
        else:
            messages.error(request, 'Both username and password are required.')
            print("Both username and password are required.")

    return render(request, 'login.html')

@login_required
def dashboard(request):
    print("Executing dashboard view")
    emails = Email.objects.filter(recipients__email=request.user.email).distinct().select_related('sender')
    print(f"Retrieved {len(emails)} emails for user {request.user.username}")
    for email in emails:
        print(f"Email Subject: {email.subject}, Sender: {email.sender.username}")
    return render(request, 'dashboard.html', {'emails': emails})

@login_required
def send_email(request):
    if request.method == 'POST':
        try:
            recipient_emails = request.POST.get('recipient')
            subject = request.POST.get('subject')
            body = request.POST.get('body')
            attachments = request.FILES.getlist('attachments')  # Retrieve uploaded files

            if recipient_emails and subject and body:
                sender = request.user

                recipients = []
                for email in recipient_emails.split(','):
                    recipient, created = Recipient.objects.get_or_create(email=email.strip())
                    recipients.append(recipient)

                # Create the email object
                email = Email.objects.create(
                    sender=sender,
                    subject=subject,
                    body=body,
                )

                # Set recipients for the email
                email.recipients.set(recipients)

                # Handle attachments
                for att in attachments:
                    # Create each attachment manually, associating it with the email
                    Attachment.objects.create(email=email, file=att)

                email.save()

                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'All fields are required.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return render(request, 'send_email.html')

@login_required
def email_list(request):
    folder = request.GET.get('folder', 'inbox')
    user = request.user

    if folder == 'inbox':
        emails = Email.objects.filter(recipients__email=user.email).distinct().select_related('sender')
    elif folder == 'sent':
        emails = Email.objects.filter(sender=user).distinct().select_related('sender')
    else:
        emails = Email.objects.all().distinct().select_related('sender')

    email_data = emails.values('id', 'sender__username', 'subject', 'body', 'timestamp')
    return JsonResponse(list(email_data), safe=False)

def compose_email(request):
    return render(request, 'send_email.html')


@login_required
def email_search(request):
    query = request.GET.get('q', '')
    if query:
        emails = Email.objects.filter(subject__icontains(query)).values('id', 'sender__username', 'subject', 'body', 'timestamp')
        return JsonResponse(list(emails), safe=False)
    return JsonResponse([], safe=False)

def read_email(request, email_id):
    email = get_object_or_404(Email, pk=email_id)
    attachments = email.attachment_set.all()  # Assuming your Attachment model has a ForeignKey to Email
    return render(request, 'read_email.html', {'email': email, 'attachments': attachments})

# def delete_emails(request):
#     try:
#         data = json.loads(request.body)
#         email_ids = data.get('email_ids', [])
#         Email.objects.filter(id__in=email_ids).delete() 
#         return JsonResponse({'status': 'success'})
#     except Exception as e:
#         return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def delete_emails(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email_ids = data.get('email_ids', [])

            # Perform the deletion logic here
            # For example, assuming you have an Email model:
            # Email.objects.filter(id__in=email_ids).delete()

            # Respond with success
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

def logout_view(request):
    print("Executing logout_view")
    logout(request)
    return redirect('login')
