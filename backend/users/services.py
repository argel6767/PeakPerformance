import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from datetime import timedelta
from .models import TwoFactorCode, PasswordResetToken

class UserEmailService:
    @staticmethod
    def generate_2fa_code():
        """Generate a random 6-digit code"""
        return ''.join(random.choices(string.digits, k=6))
    
    @staticmethod
    def generate_reset_token():
        """Generate a random token for password reset"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=64))
    
    @staticmethod
    def send_2fa_code(user):
        """Send a 2FA code to the user's email"""
        code = UserEmailService.generate_2fa_code()
        
        TwoFactorCode.objects.filter(user=user).delete()
        
        expiry = timezone.now() + timedelta(minutes=10)
        TwoFactorCode.objects.create(
            user=user,
            code=code,
            expires_at=expiry
        )
        
        context = {
            'user': user,
            'code': code,
            'expiry_minutes': 10
        }
        
        html_message = render_to_string('users/email/two_factor_code.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject='Your Authentication Code',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_password_reset(user):
        """Send a password reset link to the user's email"""
        token = UserEmailService.generate_reset_token()
        
        PasswordResetToken.objects.filter(user=user).delete()
        
        expiry = timezone.now() + timedelta(hours=1)
        PasswordResetToken.objects.create(
            user=user,
            token=token,
            expires_at=expiry
        )
        
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}"
        
        context = {
            'user': user,
            'reset_url': reset_url,
            'expiry_hours': 1
        }
        
        html_message = render_to_string('users/email/password_reset.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject='Password Reset Request',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )