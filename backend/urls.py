"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.contrib import admin
from django.urls import path,include

from rest_framework.authtoken.views import obtain_auth_token
import api
# from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from dj_rest_auth.views import PasswordResetConfirmView
from api.serializer import User
from api.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('auth/',obtain_auth_token),
    path('',include('api.urls')),
    # path('rest-auth/google/', GoogleLogin.as_view(), name='google_login')
    # path('auth/user/',include('api.urls'))
    # path('accounts/', include('allauth.urls')),
    # path('auth/', include('rest_auth.urls'))  # here
    # path('auth/', include('rest_framework_social_oauth2.urls')),
    # path('api/login/', include('rest_social_auth.urls_jwt_pair')),
    path('rest-auth/',include('dj_rest_auth.urls')),
    path('rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('rest-auth/logout/', BlacklistRefreshView.as_view(), name="logout"),
    # url(r'^rest-auth/registration/account-confirm-mail/',ConfirmationEmailView.as_view(), name='account_email_verification_sent'),
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('rest-auth/facebook/', FacebookLogin.as_view(), name='facebook_login'),
    path('rest-auth/delete/', UserDetailApiView.as_view(), name='delete'),
    path('accounts/', include('allauth.urls')),
    path('rest-auth/password/reset/confirm/<str:uidb64>/<str:token>', PasswordResetConfirmView.as_view(),
            name='password_reset_confirm'),
    # path('rest-auth/account-confirm-email/', VerifyEmailView.as_view(),
    #         name='account_verify_email'),
    # path('rest-auth/registration/account-confirm-email/<str:key>', ConfirmEmailView.as_view(),
    #         name='account_confirm_email'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)