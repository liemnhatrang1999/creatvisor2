from multiprocessing.context import DefaultContext
from django.db import router
from django.urls import path,include
from .views import *
from api import views
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('atelier',AtelierViews)
# router.register('client',ClientViews)
# router.register('consultant',ConsultantViews)

urlpatterns = [
    path('api/',views.ClientViews.as_view({
    'get': 'list',
    'post': 'create'
}))]