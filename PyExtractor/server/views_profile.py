from django.shortcuts import render
from django.contrib.auth import authenticate

from server.models import Account
from server import views


def profile_view(request):
    # Authentication check
    authentication_result = views.authentication_check(request)
    if authentication_result is not None:
        return authentication_result
    # Get template data from session
    template_data = views.parse_session(request)
    # Proceed with rest of the view
    return render(request, 'profile.html', template_data)