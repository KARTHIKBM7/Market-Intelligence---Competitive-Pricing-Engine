import smtplib
from email.message import EmailMessage
import os

def send_email_alert(product_name, current_price, link):
    """
    Sends an email alert when a price drop is detected.
    """
    try:
        # 1. Load Credentials (Smart-Load: Check Local first, then Cloud)
        try:
            import config
            sender = config.EMAIL_SENDER
            password = config.EMAIL_PASSWORD
            receiver = config.EMAIL_RECEIVER
        except ImportError:
            # If config.py is missing (like on GitHub Actions), use Environment Variables
            sender = os.getenv("EMAIL_SENDER")
            password = os.getenv("EMAIL_PASSWORD")
            receiver = os.getenv("EMAIL_RECEIVER")

        # 2. Create the Email content
        msg = EmailMessage()
        msg['Subject'] = f"🚨 PRICE DROP ALERT: {product_name}"
        msg['From'] = sender
        msg['To'] = receiver
        
        body = f"""
        Good news! We found a price drop.
        
        📦 Product: {product_name}
        💰 New Price: £{current_price}
        
        👉 Buy Now: {link}
        
        (This is an automated message from your Market Scraper Bot)
        """
        msg.set_content(body)

        # 3. Connect to Gmail and Send
        # Port 465 is the standard secure port for SMTP SSL
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
            
        print(f"✅ Alert sent to {receiver}!")
        return True

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False