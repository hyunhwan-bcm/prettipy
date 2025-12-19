"""
Example: Using the Kindle delivery feature

This script demonstrates how to send generated PDFs directly to your Kindle device.
"""

import os
from prettipy import PrettipyConverter, send_to_kindle, KindleDeliveryError

# Example 1: Generate PDF and send to Kindle using environment variables
print("Example 1: Generate PDF and send to Kindle")
print("-" * 50)

# Set up environment variables (in practice, set these in your shell or .env file)
# os.environ['KINDLE_EMAIL'] = 'yourname@kindle.com'
# os.environ['SMTP_USER'] = 'your.email@gmail.com'
# os.environ['SMTP_PASS'] = 'your-app-password'

# Generate a PDF from Python files
converter = PrettipyConverter()
output_file = "my_code.pdf"

try:
    # Convert current directory to PDF
    converter.convert_directory(".", output=output_file)
    
    # Send the PDF to Kindle (uses environment variables)
    # send_to_kindle(output_file)
    
    print(f"\n✓ PDF generated and ready to send: {output_file}")
    print("Uncomment the send_to_kindle line and set environment variables to actually send")
    
except Exception as e:
    print(f"Error: {e}")


# Example 2: Send to Kindle with explicit parameters
print("\n\nExample 2: Send to Kindle with explicit credentials")
print("-" * 50)

try:
    # Send with explicit parameters (more secure than hardcoding)
    # send_to_kindle(
    #     pdf_path=output_file,
    #     kindle_email="yourname@kindle.com",
    #     smtp_user="your.email@gmail.com",
    #     smtp_pass="your-app-password",
    #     subject="My Python Code Collection"
    # )
    
    print("Example code shown above (uncomment to use)")
    
except KindleDeliveryError as e:
    print(f"Delivery error: {e}")


# Example 3: Using custom SMTP server
print("\n\nExample 3: Using custom SMTP server")
print("-" * 50)

try:
    # For non-Gmail SMTP servers
    # send_to_kindle(
    #     pdf_path=output_file,
    #     kindle_email="yourname@kindle.com",
    #     smtp_user="user@custom-domain.com",
    #     smtp_pass="password",
    #     smtp_host="smtp.custom-domain.com",
    #     smtp_port=587
    # )
    
    print("Example code shown above (uncomment to use)")
    
except KindleDeliveryError as e:
    print(f"Delivery error: {e}")


print("\n\n" + "=" * 50)
print("Setup Instructions:")
print("=" * 50)
print("""
1. Find Your Kindle Email:
   - Go to Amazon Account Settings
   - Navigate to "Content and Devices" > "Preferences"
   - Find your Kindle email (e.g., yourname@kindle.com)

2. Approve Sender Email:
   - In the same settings page
   - Under "Personal Document Settings"
   - Add your sender email to the approved list

3. Get App Password (for Gmail):
   - Go to Google Account Settings
   - Security > 2-Step Verification > App passwords
   - Generate an app password for "Mail"

4. Set Environment Variables:
   export KINDLE_EMAIL="yourname@kindle.com"
   export SMTP_USER="your.email@gmail.com"
   export SMTP_PASS="your-app-password"

5. Run Your Script:
   The PDF will be delivered to your Kindle within minutes!
""")
