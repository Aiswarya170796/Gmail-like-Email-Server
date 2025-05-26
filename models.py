from django.db import models
from django.contrib.auth.models import User

class Recipient(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class Email(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_emails')
    recipients = models.ManyToManyField(Recipient, related_name='received_emails')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    unread = models.BooleanField(default=True)

    def __str__(self):
        return f'Subject: {self.subject} - From: {self.sender.username}'

class Attachment(models.Model):
    email = models.ForeignKey(Email, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/')

    def __str__(self):
        return f"Attachment for {self.email.subject}"
