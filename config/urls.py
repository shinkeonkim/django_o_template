from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include


def dummy_main(request):
    return render(request, 'main/index.html')


urlpatterns = [
    path('', dummy_main),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', 'users')),
]
