import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Optional

class EmailService:
    def __init__(self):
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('SMTP_FROM_EMAIL', self.smtp_user)
        
    async def send_email(self, to_email: str, subject: str, body: str, body_html: Optional[str] = None):
        """Send email using SMTP"""
        try:
            # If SMTP credentials not configured, skip email sending
            if not self.smtp_user or not self.smtp_password:
                print(f"SMTP not configured. Email would have been sent to {to_email}")
                return True
            
            message = MIMEMultipart('alternative')
            message['From'] = self.from_email
            message['To'] = to_email
            message['Subject'] = subject
            
            # Attach plain text
            part1 = MIMEText(body, 'plain')
            message.attach(part1)
            
            # Attach HTML if provided
            if body_html:
                part2 = MIMEText(body_html, 'html')
                message.attach(part2)
            
            # Send email
            await aiosmtplib.send(
                message,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_user,
                password=self.smtp_password,
                start_tls=True,
            )
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
    
    async def send_contact_notification(self, admin_email: str, contact_data: dict):
        """Send notification to admin about new contact form submission"""
        subject = f"New Contact Form Submission from {contact_data['name']}"
        
        body = f"""
New Contact Form Submission

Name: {contact_data['name']}
Email: {contact_data['email']}
Phone: {contact_data['phone']}

Message:
{contact_data['message']}

Submitted at: {contact_data.get('created_at', 'N/A')}
"""
        
        body_html = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f4f4f4;">
        <div style="background-color: #fff; padding: 30px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h2 style="color: #DC2626; margin-bottom: 20px;">New Contact Form Submission</h2>
            <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
                <p><strong>Name:</strong> {contact_data['name']}</p>
                <p><strong>Email:</strong> <a href="mailto:{contact_data['email']}">{contact_data['email']}</a></p>
                <p><strong>Phone:</strong> {contact_data['phone']}</p>
            </div>
            <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px;">
                <p><strong>Message:</strong></p>
                <p style="white-space: pre-wrap;">{contact_data['message']}</p>
            </div>
            <p style="margin-top: 20px; color: #666; font-size: 12px;">Submitted at: {contact_data.get('created_at', 'N/A')}</p>
        </div>
    </div>
</body>
</html>
"""
        
        return await self.send_email(admin_email, subject, body, body_html)
    
    async def send_reservation_notification(self, admin_email: str, reservation_data: dict):
        """Send notification to admin about new reservation"""
        subject = f"New Table Reservation from {reservation_data['name']}"
        
        body = f"""
New Table Reservation

Name: {reservation_data['name']}
Email: {reservation_data['email']}
Phone: {reservation_data['phone']}

Reservation Details:
Date: {reservation_data['date']}
Time: {reservation_data['time']}
Number of Guests: {reservation_data['guests']}

Special Requests:
{reservation_data.get('special_requests', 'None')}

Submitted at: {reservation_data.get('created_at', 'N/A')}
"""
        
        body_html = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f4f4f4;">
        <div style="background-color: #fff; padding: 30px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h2 style="color: #DC2626; margin-bottom: 20px;">New Table Reservation</h2>
            <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
                <p><strong>Name:</strong> {reservation_data['name']}</p>
                <p><strong>Email:</strong> <a href="mailto:{reservation_data['email']}">{reservation_data['email']}</a></p>
                <p><strong>Phone:</strong> {reservation_data['phone']}</p>
            </div>
            <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #DC2626; margin-bottom: 10px;">
                <p><strong>Date:</strong> {reservation_data['date']}</p>
                <p><strong>Time:</strong> {reservation_data['time']}</p>
                <p><strong>Number of Guests:</strong> {reservation_data['guests']}</p>
            </div>
            {f'<div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px;"><p><strong>Special Requests:</strong></p><p style="white-space: pre-wrap;">{reservation_data.get("special_requests", "None")}</p></div>' if reservation_data.get('special_requests') else ''}
            <p style="margin-top: 20px; color: #666; font-size: 12px;">Submitted at: {reservation_data.get('created_at', 'N/A')}</p>
        </div>
    </div>
</body>
</html>
"""
        
        return await self.send_email(admin_email, subject, body, body_html)
