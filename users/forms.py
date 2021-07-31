import os
from django.core.exceptions import ValidationError

from django.db.models import fields
from django.forms.widgets import CheckboxInput
from users.models import User, UserManager
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail

from .tokens import user_activation_token_generator


class BaseCreationForm(forms.ModelForm):
    """사용자 생성 폼"""
    email = forms.EmailField(
        label=_('Email'),
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Enter your email address.'),
                'required': 'True',
            }
        )
    )
    nickname = forms.CharField(
        label=_('Nickname'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Enter your nickname.'),
                'required': 'True',
            }
        )
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Enter your password.'),
            }
        )
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Confirm yout password.'),
            }
        )
    )

    class Meta:
        model = User
        fields = ('email', 'nickname')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = UserManager.normalize_email(self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class BaseEditionForm(forms.ModelForm):
    """회원 정보 변경 폼"""
    password = ReadOnlyPasswordHashField(
        label=_('Password')
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'last_name',
                  'first_name', 'is_active', 'is_superuser')

    def clean_password(self):
        return self.initial['password']


class UserCreationForm(BaseCreationForm):
    terms = forms.BooleanField(
        label=_('Terms of service'),
        widget=forms.CheckboxInput(
            attrs={
                'required': 'True',
            }
        ),
        error_messages={
            'required': _('You must agree to the Terms of service to sign up'),
        }
    )

    privacy = forms.BooleanField(
        label=_('Privacy policy'),
        widget=forms.CheckboxInput(
            attrs={
                'required': 'True',
            }
        ),
        error_messages={
            'required': _('You must agree to the Privacy policy to sign up')
        }
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('request')
        super(UserCreationForm, self).__init__(*args, **kwargs)

    def save(self, current_site, commit=True):
        user = super(UserCreationForm, self).save(commit=False)

        if commit:
            user.save()

            subject = _(f'Welcome To {current_site.name}! Confirm Your Email')
            message = render_to_string(
                'mailers/activation.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': user_activation_token_generator.make_token(user),
                }
            )

            send_mail(
                subject,
                message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
                html_message=message,
            )


class UserAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                _("This account is inactive."),
                code='inactive',
            )
