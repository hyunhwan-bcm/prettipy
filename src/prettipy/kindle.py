"""
Kindle delivery module for Prettipy.

This module provides functionality to send generated PDFs directly to Kindle
devices via the Send to Kindle email service.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path
from typing import Optional


class KindleDeliveryError(Exception):
    """Exception raised for errors in Kindle delivery."""
    pass


def send_to_kindle(
    pdf_path: str,
    kindle_email: Optional[str] = None,
    smtp_user: Optional[str] = None,
    smtp_pass: Optional[str] = None,
    smtp_host: str = "smtp.gmail.com",
    smtp_port: int = 587,
    subject: Optional[str] = None
) -> None:
    """
    Send a PDF file to a Kindle device via email.

    This function uses the Send to Kindle email service to deliver PDFs.
    Amazon allows users to email documents to their personal @kindle.com address.

    **Setup Requirements:**
    1. Find your Kindle email address in your Amazon account settings
       (e.g., yourname@kindle.com)
    2. Add your sender email to the approved list in Amazon account settings
       under "Personal Document Settings"
    3. Enable "less secure app access" or use an app-specific password if using Gmail

    Args:
        pdf_path: Path to the PDF file to send
        kindle_email: Recipient Kindle email address (e.g., 'yourname@kindle.com').
                     If None, uses KINDLE_EMAIL environment variable.
        smtp_user: SMTP username (usually your email address).
                   If None, uses SMTP_USER environment variable.
        smtp_pass: SMTP password or app-specific password.
                   If None, uses SMTP_PASS environment variable.
        smtp_host: SMTP server hostname (default: smtp.gmail.com for Gmail)
        smtp_port: SMTP server port (default: 587 for TLS)
        subject: Email subject line (default: "Convert")

    Raises:
        KindleDeliveryError: If required credentials are missing or delivery fails
        FileNotFoundError: If the PDF file doesn't exist

    Example:
        >>> # Using environment variables
        >>> send_to_kindle("output.pdf")
        
        >>> # Using explicit parameters
        >>> send_to_kindle(
        ...     pdf_path="output.pdf",
        ...     kindle_email="yourname@kindle.com",
        ...     smtp_user="your.email@gmail.com",
        ...     smtp_pass="your-app-password"
        ... )

    Environment Variables:
        KINDLE_EMAIL: Default Kindle email address
        SMTP_USER: Default SMTP username
        SMTP_PASS: Default SMTP password

    Notes:
        - Amazon's Send to Kindle service supports PDF files
        - Maximum file size is typically 50MB per document
        - Documents appear in your Kindle library within minutes
        - For Gmail, you may need to use an app-specific password
    """
    # Validate PDF file exists
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if not pdf_file.is_file():
        raise KindleDeliveryError(f"Path is not a file: {pdf_path}")

    # Get credentials from parameters or environment variables
    kindle_email = kindle_email or os.environ.get('KINDLE_EMAIL')
    smtp_user = smtp_user or os.environ.get('SMTP_USER')
    smtp_pass = smtp_pass or os.environ.get('SMTP_PASS')

    # Validate required credentials
    if not kindle_email:
        raise KindleDeliveryError(
            "Kindle email address is required. "
            "Provide via kindle_email parameter or KINDLE_EMAIL environment variable."
        )

    if not smtp_user:
        raise KindleDeliveryError(
            "SMTP username is required. "
            "Provide via smtp_user parameter or SMTP_USER environment variable."
        )

    if not smtp_pass:
        raise KindleDeliveryError(
            "SMTP password is required. "
            "Provide via smtp_pass parameter or SMTP_PASS environment variable."
        )

    # Validate email format
    if '@' not in kindle_email or not kindle_email.endswith('.com'):
        raise KindleDeliveryError(
            f"Invalid Kindle email format: {kindle_email}"
        )

    # Create message
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = kindle_email
    msg['Subject'] = subject or "Convert"

    # Add body text
    body = "Please find attached PDF for your Kindle."
    msg.attach(MIMEText(body, 'plain'))

    # Attach PDF file
    try:
        with open(pdf_file, 'rb') as attachment:
            part = MIMEBase('application', 'pdf')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {pdf_file.name}'
            )
            msg.attach(part)
    except Exception as e:
        raise KindleDeliveryError(f"Failed to read PDF file: {e}")

    # Send email
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        
        print(f"✓ Successfully sent {pdf_file.name} to {kindle_email}")
    except smtplib.SMTPAuthenticationError:
        raise KindleDeliveryError(
            "SMTP authentication failed. Check your username and password. "
            "For Gmail, you may need to use an app-specific password."
        )
    except smtplib.SMTPException as e:
        raise KindleDeliveryError(f"Failed to send email: {e}")
    except Exception as e:
        raise KindleDeliveryError(f"Unexpected error during delivery: {e}")
