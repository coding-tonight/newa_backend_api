from django.urls import path 

from rest_framework_simplejwt.views import TokenRefreshView

from app.views import LoginApiView, RegisterApiView


urlpatterns = [
    # ....
    path('login/', LoginApiView.as_view(), name='login'),
    path('register/', RegisterApiView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

