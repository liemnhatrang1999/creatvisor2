
from django.db import router
from django.urls import path,include,re_path
from .views import *
from api import views
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register('atelier',AtelierView,basename='Atelier')
router.register('info/entrepreneur',Info_entrepreneurView,basename='info_entrepreneur')
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
#     path('api/',views.ClientViews.as_view({
#     'get' : 'list'  , 
#     'post': 'create'

# }))]
    path('api/register',RegisterView.as_view()),
    path('api/profile',RetrieveView.as_view()),
    path('api/profile/upload',Info_entrepreneurView.as_view({
        'get' : 'list',
        'post' : 'create',
    })),
    path('api/profile/upload/<int:pk>',Info_entrepreneurView.as_view({
        'put' : 'update',
        'get' : 'retrieve',
        'delete' : 'destroy',
    })),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('',include(router.urls)),
    path('api/atelier/<int:pk>',DetailAtelier.as_view()),

    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$',  
    #     RegisterView.activate, name='activate'),  
    re_path(
        r'^activate/(?P<uidb64>[^/]+)/(?P<token>[0-9A-Za-z]{1,13}-\w{1,32})/',
        RegisterView.activate,
        name='activate'
),
    # path('activate',  
    #      RegisterView.activate, name='activate'), 
]



#     # path('api/login/',views.login),
    