document.addEventListener('DOMContentLoaded', function () {
    // Load dashboard emails by default
    loadEmails('dashboard');

    // Handle folder navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const folder = this.dataset.folder;
            loadEmails(folder);
        });
    });

    // Handle email search
    document.getElementById('searchForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const searchQuery = document.getElementById('searchInput').value.trim();
        if (searchQuery !== '') {
            searchEmails(searchQuery);
        }
    });

    // Handle email refresh
    document.querySelector('.bi-arrow-clockwise').addEventListener('click', function() {
        alert('Refreshing...'); // Replace with actual refresh logic
        loadEmails('dashboard');
    });

    // Handle sending email
   
document.getElementById('sendButton').addEventListener('click', function() {
    const form = document.getElementById('composeForm');
    const url = form.action; // Retrieve the form action URL
    const formData = new FormData(form); // Collect form data

    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': '{{ csrf_token }}' // Include CSRF token for Django
        }
    })
    .then(response => {
        if (response.ok) {
            // Handle success, e.g., show a success message or redirect
            alert('Email sent successfully!');
            $('#composeModal').modal('hide'); // Hide modal on success
            form.reset(); // Optional: Reset the form fields
        } else {
            // Handle errors or failure cases
            alert('Failed to send email. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error sending email:', error);
        alert('Failed to send email. Please check your network connection.');
    });
});


function loadEmails(folder) {
    fetch(`/emails/${folder}`)
        .then(response => response.json())
        .then(data => {
            const emailList = document.getElementById('email-list');
            emailList.innerHTML = ''; // Clear previous emails
            data.forEach(email => {
                const emailItem = document.createElement('div');
                emailItem.className = 'email-item row';
                emailItem.style.cursor = 'pointer';
                emailItem.onclick = function() {
                    showEmailContent(email.id);
                };
                emailItem.innerHTML = `
                    <div class="col-md-3">
                        <input type="checkbox">
                        <span class="sender">${folder === 'sent' ? 'To: ' + email.recipient : 'From: ' + email.sender}</span>
                    </div>
                    <div class="col-md-6">
                        <span class="subject">${email.subject}</span>
                        <span class="snippet">${email.body.substring(0, 50)}</span>
                    </div>
                    <div class="col-md-3 text-right">
                        <span class="date">${new Date(email.timestamp).toLocaleString()}</span>
                    </div>
                `;
                emailList.appendChild(emailItem);
            });
        })
        .catch(error => console.error('Error loading emails:', error));
}

function showEmailContent(emailId) {
    fetch(`/email/${emailId}`)
        .then(response => response.json())
        .then(data => {
            const emailContent = document.getElementById('email-content');
            emailContent.innerHTML = `
                <div class="col-md-3 sender">${data.sender || data.recipient}</div>
                <div class="col-md-6">
                    <div class="subject">${data.subject}</div>
                    <div class="body">${data.body}</div>
                </div>
                <div class="col-md-3 text-right timestamp">${new Date(data.timestamp).toLocaleString()}</div>
            `;
            emailContent.style.display = 'block';
        })
        .catch(error => console.error('Error loading email content:', error));
}

function searchEmails(query) {
    const url = `/send_email/?search=${encodeURIComponent(query)}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            displayEmails(data);
        })
        .catch(error => console.error('Error searching emails:', error));
}

function displayEmails(emails) {
    const emailList = document.getElementById('email-list');
    emailList.innerHTML = ''; // Clear any existing content
    emails.forEach(email => {
        const emailItem = document.createElement('div');
        emailItem.className = 'email-item';
        const fontWeight = email.unread ? 'bold' : 'normal';
        emailItem.innerHTML = `
            <div class="row" style="cursor: pointer;" onclick="openEmail(${email.id})">
                <div class="col-md-3">
                    <input type="checkbox">
                    <span class="sender" style="font-weight: ${fontWeight};">${email.sender}</span>
                </div>
                <div class="col-md-6">
                    <span class="subject" style="font-weight: ${fontWeight};">${email.subject}</span>
                    <span class="snippet" style="font-weight: ${fontWeight};">${email.body.substring(0, 50)}</span>
                </div>
                <div class="col-md-3 text-right">
                    <span class="date" style="font-weight: ${fontWeight};">${new Date(email.timestamp).toLocaleString()}</span>
                </div>
            </div>
        `;
        emailList.appendChild(emailItem);
    });
}
