from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

    (r'^auth/', include('django_odesk.auth.urls')),
    (r'^accounts/$', 'django.contrib.auth.views.login'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),

    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^$', 'otter.main.views.home'),

)

if settings.SERVE_STATIC_FILES:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
            {'document_root': settings.MEDIA_ROOT}),
    )
