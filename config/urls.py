from django.contrib import admin
from django.conf import settings
from django.shortcuts import render
from django.views.static import serve
from django.urls import path, include, re_path
from django.conf.urls.static import static
import debug_toolbar


from django.contrib import messages


def dummy_main(request):
    messages.success(request, 'test toast message')
    return render(request, 'main/index.html')


urlpatterns = [
    path('', dummy_main),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', 'users')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('explorer/', include('explorer.urls')),
    path("unicorn/", include("django_unicorn.urls")),
    path('silk/', include('silk.urls', 'silk')),
    re_path(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_ROOT}),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
