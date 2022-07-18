
from django.db import router
from django.urls import path,include
from .views import *
from api import views
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('atelier',AtelierViews)
# router.register('client',ClientViews)
# router.register('consultant',ConsultantViews)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
#     path('api/',views.ClientViews.as_view({
#     'get' : 'list'  , 
#     'post': 'create'

# }))]
    path('register',RegisterView.as_view()),
    path('me',RetrieveView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]



#     # path('api/login/',views.login),
    