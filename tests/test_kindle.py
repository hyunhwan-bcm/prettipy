"""Tests for the Kindle delivery module."""

import pytest
import os
import smtplib
from pathlib import Path
from unittest.mock import patch, MagicMock
from prettipy.kindle import send_to_kindle, KindleDeliveryError


class TestKindleDelivery:
    """Test cases for Kindle PDF delivery functionality."""

    def test_send_to_kindle_missing_pdf_file(self):
        """Test that send_to_kindle raises error for non-existent file."""
        with pytest.raises(FileNotFoundError):
            send_to_kindle(
                pdf_path="/nonexistent/file.pdf",
                kindle_email="test@kindle.com",
                smtp_user="user@example.com",
                smtp_pass="password"
            )

    def test_send_to_kindle_missing_kindle_email(self, tmp_path):
        """Test that send_to_kindle raises error when Kindle email is missing."""
        # Create a temporary PDF file
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 test content")

        with pytest.raises(KindleDeliveryError) as exc_info:
            send_to_kindle(
                pdf_path=str(pdf_file),
                smtp_user="user@example.com",
                smtp_pass="password"
            )
        
        assert "Kindle email address is required" in str(exc_info.value)

    def test_send_to_kindle_missing_smtp_user(self, tmp_path):
        """Test that send_to_kindle raises error when SMTP user is missing."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 test content")

        with pytest.raises(KindleDeliveryError) as exc_info:
            send_to_kindle(
                pdf_path=str(pdf_file),
                kindle_email="test@kindle.com",
                smtp_pass="password"
            )
        
        assert "SMTP username is required" in str(exc_info.value)

    def test_send_to_kindle_missing_smtp_pass(self, tmp_path):
        """Test that send_to_kindle raises error when SMTP password is missing."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 test content")

        with pytest.raises(KindleDeliveryError) as exc_info:
            send_to_kindle(
                pdf_path=str(pdf_file),
                kindle_email="test@kindle.com",
                smtp_user="user@example.com"
            )
        
        assert "SMTP password is required" in str(exc_info.value)

    def test_send_to_kindle_invalid_email_format(self, tmp_path):
        """Test that send_to_kindle raises error for invalid email format."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 test content")

        with pytest.raises(KindleDeliveryError) as exc_info:
            send_to_kindle(
                pdf_path=str(pdf_file),
                kindle_email="invalid-email",
                smtp_user="user@example.com",
                smtp_pass="password"
            )
        
        assert "Invalid Kindle email format" in str(exc_info.value)

    def test_send_to_kindle_not_a_file(self, tmp_path):
        """Test that send_to_kindle raises error when path is a directory."""
        # Create a directory instead of a file
        pdf_dir = tmp_path / "test.pdf"
        pdf_dir.mkdir()

        with pytest.raises(KindleDeliveryError) as exc_info:
            send_to_kindle(
                pdf_path=str(pdf_dir),
                kindle_email="test@kindle.com",
                smtp_user="user@example.com",
                smtp_pass="password"
            )
        
        assert "Path is not a file" in str(exc_info.value)

    @patch('prettipy.kindle.smtplib.SMTP')
    def test_send_to_kindle_success(self, mock_smtp, tmp_path):
        """Test successful PDF delivery to Kindle."""
        # Create a temporary PDF file
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 test content")

        # Mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        # Call function
        send_to_kindle(
            pdf_path=str(pdf_file),
            kindle_email="test@kindle.com",
            smtp_user="user@example.com",
            smtp_pass="password"
        )

        # Verify SMTP was called correctly
        mock_smtp.assert_called_once_with("smtp.gmail.com", 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("user@example.com", "password")
        mock_server.send_message.assert_called_once()

    @patch('prettipy.kindle.smtplib.SMTP')
    def test_send_to_kindle_with_custom_smtp(self, mock_smtp, tmp_path):
        """Test PDF delivery with custom SMTP server settings."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 test content")

        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        send_to_kindle(
            pdf_path=str(pdf_file),
            kindle_email="test@kindle.com",
            smtp_user="user@example.com",
            smtp_pass="password",
            smtp_host="smtp.custom.com",
            smtp_port=465
        )

        mock_smtp.assert_called_once_with("smtp.custom.com", 465)

    @patch('prettipy.kindle.smtplib.SMTP')
    def test_send_to_kindle_with_custom_subject(self, mock_smtp, tmp_path):
        """Test PDF delivery with custom email subject."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 test content")

        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        send_to_kindle(
            pdf_path=str(pdf_file),
            kindle_email="test@kindle.com",
            smtp_user="user@example.com",
            smtp_pass="password",
            subject="My Custom Document"
        )

        # Verify send_message was called
        mock_server.send_message.assert_called_once()

    @patch.dict(os.environ, {
        'KINDLE_EMAIL': 'env@kindle.com',
        'SMTP_USER': 'envuser@example.com',
        'SMTP_PASS': 'envpassword'
    })
    @patch('prettipy.kindle.smtplib.SMTP')
    def test_send_to_kindle_from_environment(self, mock_smtp, tmp_path):
        """Test that send_to_kindle reads from environment variables."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 test content")

        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        # Call without parameters - should use environment variables
        send_to_kindle(pdf_path=str(pdf_file))

        mock_server.login.assert_called_once_with("envuser@example.com", "envpassword")

    @patch('prettipy.kindle.smtplib.SMTP')
    def test_send_to_kindle_smtp_auth_error(self, mock_smtp, tmp_path):
        """Test handling of SMTP authentication errors."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 test content")

        mock_server = MagicMock()
        mock_server.login.side_effect = smtplib.SMTPAuthenticationError(535, b'Auth failed')
        mock_smtp.return_value.__enter__.return_value = mock_server

        with pytest.raises(KindleDeliveryError) as exc_info:
            send_to_kindle(
                pdf_path=str(pdf_file),
                kindle_email="test@kindle.com",
                smtp_user="user@example.com",
                smtp_pass="wrong_password"
            )
        
        assert "SMTP authentication failed" in str(exc_info.value)

    @patch('prettipy.kindle.smtplib.SMTP')
    def test_send_to_kindle_smtp_general_error(self, mock_smtp, tmp_path):
        """Test handling of general SMTP errors."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4 test content")

        mock_server = MagicMock()
        mock_server.send_message.side_effect = smtplib.SMTPException("Connection error")
        mock_smtp.return_value.__enter__.return_value = mock_server

        with pytest.raises(KindleDeliveryError) as exc_info:
            send_to_kindle(
                pdf_path=str(pdf_file),
                kindle_email="test@kindle.com",
                smtp_user="user@example.com",
                smtp_pass="password"
            )
        
        assert "Failed to send email" in str(exc_info.value)
