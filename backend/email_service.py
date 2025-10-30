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


    async def send_order_confirmation(self, to_email: str, customer_name: str, order_id: str, 
                                     items: list, subtotal: float, tax: float, delivery_fee: float, 
                                     total: float, delivery_address: str, payment_method: str):
        """Send order confirmation email to customer"""
        subject = f"Order Confirmation - {order_id}"
        
        # Build items list for plain text
        items_text = "\n".join([
            f"  • {item['name']} x{item['quantity']} - ${item['subtotal']:.2f}"
            for item in items
        ])
        
        body = f"""
Dear {customer_name},

Thank you for your order! We have received your order and will start preparing it shortly.

Order Details:
Order ID: {order_id}

Items Ordered:
{items_text}

Subtotal: ${subtotal:.2f}
Tax (8%): ${tax:.2f}
Delivery Fee: ${delivery_fee:.2f}
------------------------
Total: ${total:.2f}

Delivery Address:
{delivery_address}

Payment Method: {payment_method}

We'll notify you once your order is out for delivery.

Thank you for choosing Lakeside Indian Restaurant!

Best regards,
Lakeside Indian Restaurant Team
"""
        
        # Build items list for HTML
        items_html = "\n".join([
            f"""
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">{item['name']}</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">{item['quantity']}</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: right;">${item['price']:.2f}</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: right; font-weight: bold;">${item['subtotal']:.2f}</td>
            </tr>
            """
            for item in items
        ])
        
        body_html = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f4f4f4;">
        <div style="background-color: #fff; padding: 30px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #DC2626; margin: 0;">Lakeside Indian Restaurant</h1>
                <p style="color: #666; margin-top: 5px;">Order Confirmation</p>
            </div>
            
            <p>Dear <strong>{customer_name}</strong>,</p>
            <p>Thank you for your order! We have received your order and will start preparing it shortly.</p>
            
            <div style="background-color: #DC2626; color: white; padding: 15px; border-radius: 5px; margin: 20px 0; text-align: center;">
                <p style="margin: 0; font-size: 14px;">Order ID</p>
                <p style="margin: 5px 0 0 0; font-size: 24px; font-weight: bold;">{order_id}</p>
            </div>
            
            <h3 style="color: #DC2626; border-bottom: 2px solid #DC2626; padding-bottom: 10px;">Order Details</h3>
            
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                <thead>
                    <tr style="background-color: #f9f9f9;">
                        <th style="padding: 10px; text-align: left; border-bottom: 2px solid #DC2626;">Item</th>
                        <th style="padding: 10px; text-align: center; border-bottom: 2px solid #DC2626;">Qty</th>
                        <th style="padding: 10px; text-align: right; border-bottom: 2px solid #DC2626;">Price</th>
                        <th style="padding: 10px; text-align: right; border-bottom: 2px solid #DC2626;">Subtotal</th>
                    </tr>
                </thead>
                <tbody>
                    {items_html}
                </tbody>
            </table>
            
            <div style="background-color: #f9f9f9; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
                <table style="width: 100%;">
                    <tr>
                        <td style="padding: 5px 0;">Subtotal:</td>
                        <td style="padding: 5px 0; text-align: right;">${subtotal:.2f}</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px 0;">Tax (8%):</td>
                        <td style="padding: 5px 0; text-align: right;">${tax:.2f}</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px 0;">Delivery Fee:</td>
                        <td style="padding: 5px 0; text-align: right;">${delivery_fee:.2f}</td>
                    </tr>
                    <tr style="border-top: 2px solid #DC2626;">
                        <td style="padding: 10px 0; font-size: 18px; font-weight: bold;">Total:</td>
                        <td style="padding: 10px 0; text-align: right; font-size: 18px; font-weight: bold; color: #DC2626;">${total:.2f}</td>
                    </tr>
                </table>
            </div>
            
            <div style="margin-bottom: 20px;">
                <h4 style="color: #DC2626; margin-bottom: 10px;">Delivery Address:</h4>
                <p style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; white-space: pre-wrap;">{delivery_address}</p>
            </div>
            
            <div style="background-color: #d4edda; padding: 15px; border-radius: 5px; border-left: 4px solid #28a745;">
                <p style="margin: 0;"><strong>Payment Method:</strong> {payment_method}</p>
            </div>
            
            <p style="margin-top: 30px;">We'll notify you once your order is out for delivery.</p>
            
            <p>Thank you for choosing Lakeside Indian Restaurant!</p>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; text-align: center; color: #666; font-size: 12px;">
                <p>Best regards,<br>Lakeside Indian Restaurant Team</p>
            </div>
        </div>
    </div>
</body>
</html>
"""
        
        return await self.send_email(to_email, subject, body, body_html)
    
    async def send_new_order_notification(self, to_email: str, order_id: str, customer_name: str, 
                                         customer_phone: str, items: list, total: float, 
                                         delivery_address: str):
        """Send new order notification to admin"""
        subject = f"New Order Received - {order_id}"
        
        # Build items list for plain text
        items_text = "\n".join([
            f"  • {item['name']} x{item['quantity']} - ${item['subtotal']:.2f}"
            for item in items
        ])
        
        body = f"""
New Order Received!

Order ID: {order_id}

Customer Details:
Name: {customer_name}
Phone: {customer_phone}

Items:
{items_text}

Total Amount: ${total:.2f}

Delivery Address:
{delivery_address}

Please log in to the admin panel to manage this order.
"""
        
        # Build items list for HTML
        items_html = "\n".join([
            f"""
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #eee;">{item['name']}</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">{item['quantity']}</td>
                <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: right; font-weight: bold;">${item['subtotal']:.2f}</td>
            </tr>
            """
            for item in items
        ])
        
        body_html = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f4f4f4;">
        <div style="background-color: #fff; padding: 30px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <div style="background-color: #DC2626; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; text-align: center;">
                <h2 style="margin: 0;">🎉 New Order Received!</h2>
            </div>
            
            <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                <p style="margin: 0; font-size: 14px; color: #666;">Order ID</p>
                <p style="margin: 5px 0 0 0; font-size: 24px; font-weight: bold; color: #DC2626;">{order_id}</p>
            </div>
            
            <div style="margin-bottom: 20px;">
                <h3 style="color: #DC2626; margin-bottom: 10px;">Customer Details:</h3>
                <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px;">
                    <p><strong>Name:</strong> {customer_name}</p>
                    <p><strong>Phone:</strong> {customer_phone}</p>
                </div>
            </div>
            
            <h3 style="color: #DC2626; margin-bottom: 10px;">Order Items:</h3>
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                <thead>
                    <tr style="background-color: #f9f9f9;">
                        <th style="padding: 10px; text-align: left; border-bottom: 2px solid #DC2626;">Item</th>
                        <th style="padding: 10px; text-align: center; border-bottom: 2px solid #DC2626;">Qty</th>
                        <th style="padding: 10px; text-align: right; border-bottom: 2px solid #DC2626;">Subtotal</th>
                    </tr>
                </thead>
                <tbody>
                    {items_html}
                </tbody>
            </table>
            
            <div style="background-color: #DC2626; color: white; padding: 15px; border-radius: 5px; margin-bottom: 20px; text-align: center;">
                <p style="margin: 0; font-size: 14px;">Total Amount</p>
                <p style="margin: 5px 0 0 0; font-size: 28px; font-weight: bold;">${total:.2f}</p>
            </div>
            
            <div style="margin-bottom: 20px;">
                <h4 style="color: #DC2626; margin-bottom: 10px;">Delivery Address:</h4>
                <p style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; white-space: pre-wrap;">{delivery_address}</p>
            </div>
            
            <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #ffc107;">
                <p style="margin: 0;">⚠️ Please log in to the admin panel to manage this order.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""
        
        return await self.send_email(to_email, subject, body, body_html)
