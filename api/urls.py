from django.urls import path
from .views import HelloView, welcome

urlpatterns = [
    path('api/hello', HelloView.as_view(), name='hello'),
     path('', welcome, name='home'),
]