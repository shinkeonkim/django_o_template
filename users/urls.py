from django.urls import path, re_path

from .views import UserActivationView, UserSignUpView, UserSignInView, UserSignOutView, UserPasswordChangeView

app_name = 'users'

urlpatterns = [
    re_path('signup/$', UserSignUpView.as_view(), name='signup'),
    re_path('signin/$', UserSignInView.as_view(), name='signin'),
    re_path('signout/$', UserSignOutView.as_view(), name='signout'),
    re_path('password/change/$', UserPasswordChangeView.as_view(),
            name='password_change'),
    path('activate/<str:uidb64>/<str:token>/',
         UserActivationView.as_view(), name="activate"),
]
