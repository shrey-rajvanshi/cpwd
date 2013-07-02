from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout
from home.views import *
from work.views import *
from django.conf.urls.static import static
from django.views.generic import RedirectView
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('home.views',
    # Examples:
    url(r'^home/$', 'home', name='home'),
    url(r'^$','start',name = 'start'),
    url(r'^accounts/logout/$', logout),
    url(r'^accounts/login/$','start'),
    # url(r'^SKBhawan/', include('SKBhawan.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)



urlpatterns += patterns('work.views',
	url(r'^search/$','search',name = 'search'),
    url(r'^add/$','add',name = 'add'),
    url(r'^all/$','all',name = 'all'),
    url(r'^xls/$','xls',name = 'xls'),
    url(r'^edit/(?P<id>\d+)/$','edit',name = 'edit'),
    url(r'^view/(?P<id>\d+)/$','showwork',name = 'view'),
    url(r'^drawing/(?P<id>\d+)/$','draw',name = 'drawing'),
    url(r'^deldrawing/(?P<id>\d+)/$','deldrawing',name = 'deldrawing'),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    



if settings.DEBUG:
#    urlpatterns  = patterns('',
#                            url(r'^2013/', include(urlpatterns)),
#    )

    from django.views.static import serve
    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns += patterns('',
            (r'^%s(?P<path>.*)$' % _media_url,
             serve,
                 {'document_root': settings.MEDIA_ROOT}))
    del(_media_url, serve)
