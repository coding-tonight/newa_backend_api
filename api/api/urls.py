from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    # docs routes
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('', SpectacularSwaggerView.as_view(
        url_name='schema'), name='swagger-ui'),
    # end here
    # re_path(r'^auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('api/v1/', include('app.urls'))


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
