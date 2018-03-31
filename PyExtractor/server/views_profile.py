from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, HttpResponse
from server.models import Account, asset
from server import views
from server.forms import QueryForm, AssetForm

def profile_view(request):
    # Authentication check
    authentication_result = views.authentication_check(request)
    if authentication_result is not None:
    	return authentication_result
    # Get template data from session
    template_data = views.parse_session(request)
    # Proceed with rest of the view
    return render(request, 'profile.html', template_data)


def assets_view(request):
	authentication_result = views.authentication_check(request)
	if authentication_result is not None:
		return authentication_result
	template_data = views.parse_session(request)
	template_data['assets'] = asset.objects.filter(owner=request.user)
	print(template_data['assets'])
	return render(request, 'assets.html', template_data)


def delete_asset(request):
    # Authentication check
    authentication_result = views.authentication_check(request)
    if authentication_result is not None:
        return authentication_result
    # Get template data from session
    template_data = views.parse_session(request)
    # Proceed with rest of the view
    if request.method == 'POST':
        if 'delete' in request.POST and 'pk' in request.POST:
            pk = request.POST['pk']
            try:
                image = asset.objects.get(pk=pk)
            except Exception:
                template_data['alert_danger'] = "Unable to delete the image. Please try again later"
                return
            image.delete()
            template_data['alert_success'] = "The image has been deleted."
            return HttpResponseRedirect('/assets')
    template_data['alert_danger'] = "The image couldn't be deleted."
    return HttpResponseRedirect('/assets')


def update_asset(request):
    # Authentication check
    authentication_result = views.authentication_check(request, None,['pk'])
    if authentication_result is not None:
        return authentication_result

    pk = request.GET['pk']
    a = asset()
    try:
        Asset = asset.objects.get(pk=pk)
        print(Asset)
    except Exception:
        request.session['alert_danger'] = "The requested image doesn't exist"
        return HttpResponseRedirect('/error/denied')
    template_data = views.parse_session(
        request,
        {
            'form_button':"Update image asset",
            'form_action':"?pk="+pk,
            'asset':Asset
        })
    request.POST._mutable = True
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.assign(Asset)
            Asset.save()
            template_data['alert_success'] = "The asset data has been updated!"
            template_data['form'] = form
    else:
        form = AssetForm(Asset.get_populated_fields())
    template_data['form']=form
    return render(request,'asset_update.html',template_data)