from django.shortcuts import render, redirect
from django import forms

from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import CustomUserCreationForm
from .token_generator import account_activation_token

from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'signup.html'


# function for signup
def SignUpView(request):
    form = CustomUserCreationForm

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'

            message = render_to_string('activateaccount.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return redirect('accountconfirmation')
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})


# function to activate account
def activateaccount(request, uidb64, token):

    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):

        user.is_active = True
        user.save()
        login(request, user)
        # form = HomeForm()

        context = {'uidb64': uidb64, 'token': token,
                   'form': [], 'text': "Your account is activated!"}
        return render(request, 'accountactivated.html', context)
    else:
        # form = HomeForm()
        context = {'form': []}
        return render(request, 'home.html', context)


def accountconfirmation(request):
    template_name = 'accountconfirmation.html'
    return render(request, template_name)


def accountactivated(request):
    template_name = 'accountactivated.html'
    return render(request, template_name)
