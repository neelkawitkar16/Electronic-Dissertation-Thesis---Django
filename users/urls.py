from django.urls import path

# from .views import SignUpView, accountactivated, accountconfirmation, activateaccount
from . import views
#from django.conf import settings

urlpatterns = [
    path('signup/', views.SignUpView, name='signup'),
    path('accountactivated/', views.accountactivated, name='accountactivated'),
    path('activate/<uidb64>/<token>/', views.activateaccount, name='activate'),

    path('accountconfirmation/', views.accountconfirmation,
         name='accountconfirmation'),
]
