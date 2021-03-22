from django.shortcuts import render, redirect
from django import forms

from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .models import SearchResultHistoryModel, HandleModel
from .forms import CustomUserCreationForm, HomeForm, UploadForm
from .token_generator import account_activation_token
from .esETD import elasticsearchfun

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
        form = HomeForm()

        context = {'uidb64': uidb64, 'token': token,
                   'form': [], 'text': "Your account is activated!"}
        return render(request, 'accountactivated.html', context)
    else:
        form = HomeForm()
        context = {'form': []}
        return render(request, 'home.html', context)


def accountconfirmation(request):
    template_name = 'accountconfirmation.html'
    return render(request, template_name)


def accountactivated(request):
    template_name = 'accountactivated.html'
    return render(request, template_name)


class HomePageView(TemplateView):
    template_name = 'home.html'

    print("entering home page")

    def get(self, request):
        form = HomeForm()
        args = {'form': form}
        return render(request, self.template_name, args)

    # taking the input from the search page
    def post(self, request):
        form = HomeForm(request.POST)
        if form.is_valid():
            whattosearch = filtersearchtext(form)
            # saving user history if the user is loggedin
            historysave(request, form, whattosearch)
            request.session["whattosearch"] = whattosearch
            return redirect('serp')

        else:
            msg = 0
            searchtext = ""
            output = ["Not valid input"]

        args = {'form': form, 'msg': msg, 'output': output, 'text': searchtext}
        return render(request, self.template_name, args)


def historysave(request, form, whattosearch):
    if request.user.is_authenticated:
        searchhistorystore = form.save(commit=False)
        searchhistorystore.user = request.user
        searchhistorystore.searchtext = whattosearch['title']
        searchhistorystore.save()


def filtersearchtext(form):

    searchtext = form.cleaned_data['searchtext']
    whattosearch = {'title': searchtext}

    contributor_department = form.cleaned_data['contributor_department']
    if contributor_department != '':
        whattosearch['contributor_department'] = contributor_department

    contributor_author = form.cleaned_data['contributor_author']
    if contributor_author != '':
        whattosearch['contributor_author'] = contributor_author

    contributor_committeechair = form.cleaned_data['contributor_committeechair']
    if contributor_committeechair != '':
        whattosearch['contributor_committeechair'] = contributor_committeechair

    description_degree = form.cleaned_data['description_degree']
    if description_degree != '':
        whattosearch['description_degree'] = description_degree

    whattosearch['date1'] = str(form.cleaned_data['date1'])
    whattosearch['date2'] = str(form.cleaned_data['date2'])

    return whattosearch


def SERPView(request):
    template_name = 'serp.html'

    if request.method == 'GET':
        form = HomeForm()
        whattosearch = request.session["whattosearch"]
        output, msg = elasticsearchfun(whattosearch)

        searchtext = ''

        for key in whattosearch.keys():
            if key not in ['date1', 'date2']:
                searchtext = searchtext+whattosearch[key]+", "
        searchtext = searchtext+"between " + \
            whattosearch['date1']+" and "+whattosearch['date2']

        args = {'form': form, 'msg': msg, 'output': output, 'text': searchtext}
        return render(request, template_name, args)

    if request.method == 'POST':
        form = HomeForm(request.POST)
        if form.is_valid():
            whattosearch = filtersearchtext(form)
            # saving user history if the user is loggedin
            historysave(request, form, whattosearch)
            request.session["whattosearch"] = whattosearch
            return redirect('serp')
        else:
            msg = 0
            searchtext = ""
            output = ["Not valid input"]

        form = HomeForm()
        args = {'form': form, 'msg': msg, 'output': output, 'text': searchtext}
        return render(request, template_name, args)

    args = {'form': form, 'msg': 0, 'output': [
        "Some issue with SERPview"], 'text': ''}
    return render(request, template_name, args)


def SERPdetailsView(request):
    template_name = 'serpdetails.html'

    if request.method == 'GET':
        return render(request, template_name)

    if request.method == 'POST':
        handle = request.POST.get('handle', None)
        whattosearch = {"handle": handle}
        output, msg = elasticsearchfun(whattosearch, type="handlequery")

        try:
            pdfnames = output[0]["relation_haspart"]
            if str(type(pdfnames)) == "<class 'str'>":
                pdfnames = [pdfnames]

            fnames = []
            for fname in pdfnames:
                dumdict = {}
                dumdict['url'] = "http://127.0.0.1:8000/media/dissertation/" + \
                    handle+"/"+fname

                dumdict['name'] = fname
                fnames.append(dumdict)
        except:
            msg = 0
            fnames = []
            output = ["PDF files not found"]

        args = {'output': output, 'msg': msg, 'fnames': fnames}
        return render(request, template_name, args)

    return render(request, template_name)
