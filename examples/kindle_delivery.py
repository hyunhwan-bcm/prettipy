"""
Example: Using the Kindle delivery feature

This script demonstrates how to send generated PDFs directly to your Kindle device.
"""

from prettipy import PrettipyConverter, PrettipyConfig


def setup_kindle_config(kindle_email: str) -> PrettipyConfig:
    '''
    Configure Prettipy for Kindle delivery.
    
    Args:
        kindle_email: Your Kindle's email address
        
    Returns:
        Configured PrettipyConfig object
    '''
    config = PrettipyConfig(
        page_size='a4',
        max_line_width=80,
        title='Python Code Documentation',
        verbose=True
    )
    return config


def main():
    """Main function to demonstrate Kindle delivery."""
    # Replace with your Kindle email
    kindle_email = "your_kindle@kindle.com"
    
    # Setup configuration
    config = setup_kindle_config(kindle_email)
    
    # Create converter and generate PDF
    converter = PrettipyConverter(config)
    converter.convert_directory("./src", output="code_for_kindle.pdf")
    
    print(f"""
    PDF generated successfully!
    
    To send to your Kindle:
    1. Add your email to Amazon's approved list
    2. Email the PDF to {kindle_email}
    3. Wait for it to appear on your Kindle
    """)


if __name__ == "__main__":
    main()
