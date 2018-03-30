from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from server import views
from server import home
from server import upload
from server import explore
from server import views_admin, views_profile

app_name = 'server'

urlpatterns = [
	url(r'^$', home.home,name='index'),
	url(r'^login/$', home.login_view, name='login'),
	url(r'^logout/$', home.logout_view, name='logout'),
	url(r'^register/$', home.register_view, name='register'),
	url(r'^setup/$', home.setup_view, name='setup'),

	url(r'^error/denied/$', home.error_denied_view, name='error/denied'),
    
    url(r'^admin/users/$', views_admin.users_view, name='admin/users'),
    url(r'^admin/createuser/$', views_admin.createuser_view, name='admin/createuser'),

    url(r'^profile/$', views_profile.profile_view, name='profile'),


	url(r'^upload/$', upload.upload, name='upload'),
	url(r'^explore/$', explore.explore, name='explore')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)