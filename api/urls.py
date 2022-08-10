
from django.db import router
from django.urls import path,include,re_path
from .views import *
from api import views
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )


router = DefaultRouter()
router.register('atelier',AtelierView,basename='Atelier')
router.register('info/entrepreneur',Info_entrepreneurView,basename='info_entrepreneur')
router.register('info/consultant',Info_consultantView,basename='info_consultant')
router.register('avis',AvisView,basename='avis')
router.register('thematique',ThematiqueView,basename='thematique')


urlpatterns = [
    # path('api/register',RegisterView.as_view()),
    path('api/profile',RetrieveView.as_view()),
    # path('api/profile/upload',Info_entrepreneurView.as_view({
    #     'get' : 'list',
    #     'post' : 'create',
    # })),
    # path('api/profile/upload/<int:pk>',Info_entrepreneurView.as_view({
    #     'put' : 'update',
    #     'get' : 'retrieve',
    #     'delete' : 'destroy',
    # })),
    path('',include(router.urls)),
    path('api/atelier/<int:pk>',DetailAtelier.as_view()),
    re_path(
        r'^activate/(?P<uidb64>[^/]+)/(?P<token>[0-9A-Za-z]{1,13}-\w{1,32})/',
        RegisterView.activate,
        name='activate'

),
]
