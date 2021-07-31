from users.forms import UserCreationForm, UserAuthenticationForm
from django.http import request

from django.contrib import auth, messages
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.views import PasswordChangeView


from config.views import BaseTemplateView, BaseFormView, BaseView
from .models import User
from .tokens import UserActivationTokenGenerator


class UserSignUpView(BaseFormView):
    template_name = "users/signup.html"
    form_class = UserCreationForm

    def get(self, request, *args, **kwargs):
        if self.is_authenticated_user:
            return redirect('/')
        return super(UserSignUpView, self).get(self, request, *args, **kwargs)

    def form_valid(self, form):
        current_site = get_current_site(self.request)
        form.save(current_site)

        return redirect('users:signin')  # TODO: 이메일 확인하라는 메세지 추가

    def form_invalid(self, form):
        return super().form_invalid(form)


class UserSignInView(BaseFormView):
    template_name = "users/signin.html"
    form_class = UserAuthenticationForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if self.is_authenticated_user:
            return redirect('/')
        return super(UserSignInView, self).get(self, request, *args, **kwargs)

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return super().form_valid(form)


class UserSignOutView(BaseView):
    def get(self, request, *args, **kwargs):
        if self.is_authenticated_user:
            auth.logout(request)
        return redirect('/')


class UserActivationView(BaseTemplateView):
    template_name = "users/activate.html"

    def get(self, request, *args, **kwargs):
        uid = urlsafe_base64_decode(self.kwargs['uidb64']).decode()
        token = self.kwargs['token']

        self.logger.debug('uid: %s, token: %s' % (uid, token))

        try:
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            self.logger.warning('User %s not found' % uid)
            user = None

        if user is not None and UserActivationTokenGenerator().check_token(user, token):
            user.is_active = True
            user.save()
            auth.login(request, user)
            self.logger.info(
                'User %s(pk=%s) has been activated.' % (user, user.pk))
            messages.success(request, '이메일이 인증 되었습니다.')
            return redirect('/')  # TODO: 메세지 추가하기

        return super(UserActivationView, self).get(request, *args, **kwargs)


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'users/password_change.html'
    success_url = '/'
