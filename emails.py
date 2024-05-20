import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = 'alexlennon.hw@gmail.com'
sender_password = 'vdxwvehoednihmhe'

def reset_password_email(name, email, password):
    html_body = f"""
    <html>
        <body>
            <p>Dear <b>{ name }</b>, <br>
            <br>Greetings from <b>Blog Platform</b>!<br>
            <br>You have requested to reset a password. Your account has been deactivated now.<br>
            <br><b>Account Details:</b><br>
            <br><b>Email:</b> { email }
            <br><b>New Password:</b> { password }<br>
            <br>You didn't request to reset your password? Please enter your account and change your password immediately.<br>
            <br>Best regards,
            <br><strong>Blog Platform</strong>
        </body>
    </html>
    """
    email = [email]
    subject = 'Reset Password | Blog Platform'
    send_email(email, html_body, subject)

def send_email(emails, html_body, subject):
    try:
        # Create an instance of MIMEMultipart
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ", ".join(emails)
        msg['Subject'] = subject

        # Create a MIMEText part for the HTML body
        part = MIMEText(html_body, 'html')
        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(e)