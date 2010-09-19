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
    url(r'^teams/(?P<team_id>[\w\:]+)/$', 'otter.main.views.timeline',
        name='team_timeline'),
    url(r'^users/(?P<user_id>\w+)/$', 'otter.main.views.timeline',
        name='user_timeline'),
    (r'^sync/$', 'otter.main.views.sync'),

)

if settings.SERVE_STATIC_FILES:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
            {'document_root': settings.MEDIA_ROOT}),
    )
