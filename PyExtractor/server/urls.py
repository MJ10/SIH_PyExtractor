from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from server import views
from server import home
from server import upload
from server import explore


app_name = 'server'

urlpatterns = [
	url(r'^$', home.home,name='index'),
	url(r'^upload/$', upload.upload, name='upload'),
	url(r'^explore/$', explore.explore, name='explore')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)