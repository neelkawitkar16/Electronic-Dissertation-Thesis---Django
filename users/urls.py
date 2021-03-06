from django.urls import path

# from .views import SignUpView, accountactivated, accountconfirmation, activateaccount
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import delete_claim_view

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('signup/', views.SignUpView, name='signup'),
    path('accountactivated/', views.accountactivated, name='accountactivated'),
    path('activate/<uidb64>/<token>/', views.activateaccount, name='activate'),

    path('accountconfirmation/', views.accountconfirmation,
         name='accountconfirmation'),

    path('serp/', views.SERPView, name='serp'),

    path('serpdetails/', views.SERPdetailsView, name='serpdetails'),

    path('upload/', views.UploadView, name='upload'),

    path('claim/', views.ClaimSubmitView, name='claim'),

    path('delete_claim_view/', views.delete_claim_view, name='delete_claim_view'),

    path('saveitem/', views.SaveItemView, name='saveitem'),

    path('deleteitem/', views.DeleteItemView, name='deleteitem'),

    path('claimlike/', views.ClaimLikeView, name='claimlike'),

    path('autocomplete/', views.AutoCompleteView, name='autocomplete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
