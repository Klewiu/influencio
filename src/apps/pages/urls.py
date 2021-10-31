from django.urls import path
from . import views
from influencio_app import settings
from django.conf.urls.static import static
from .views import MoviesView

urlpatterns = [
    path('', MoviesView.as_view(), name='page-home'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()