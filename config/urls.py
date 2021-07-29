from django.contrib import admin
from django.conf import settings
from django.shortcuts import render
from django.views.static import serve
from django.urls import path, include, re_path
from django.conf.urls.static import static


def dummy_main(request):
    return render(request, 'main/index.html')


urlpatterns = [
    path('', dummy_main),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', 'users')),
    re_path(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_ROOT}),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
