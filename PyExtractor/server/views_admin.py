from csv import QUOTE_MINIMAL, writer
import re

from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.db.utils import IntegrityError

from server.forms import UserRegistrationForm
from server.models import Account
from server import views


def users_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_ADMIN])
    if authentication_result is not None:
        return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request)
    # Proceed with the rest of the view
    if request.method == 'POST':
        pk = request.POST['pk']
        role = request.POST['role']
        account = Account.objects.get(pk=pk)
        if account is not None:
            account.role = role
            account.save()
            template_data['alert_success'] = "Updated" + account.user.username + "'s role!"
    # Parse search sorting
    template_data['query'] = Account.objects.all().order_by('-role')
    return render(request,'admin/users.html', template_data)



def createuser_view(request):
    # Authentication check.
    authentication_result = views.authentication_check(request, [Account.ACCOUNT_ADMIN])
    if authentication_result is not None: return authentication_result
    # Get the template data from the session
    template_data = views.parse_session(request,{'form_button':"Register"})
    # Proceed with the rest of the view
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = views.register_user(
                form.cleaned_data['email'],
                form.cleaned_data['password_first'],
                form.cleaned_data['employee'],
            )
            request.session['alert_success'] = "Successfully created new user account"
            return HttpResponseRedirect('/admin/users/')
    else:
        form = UserRegistrationForm()
    template_data['form'] = form
    return render(request,'admin/createuser.html', template_data)
