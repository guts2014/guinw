from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sas.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'web.views.index'),
    # url(r'^search/', 'web.views.search'),
    url(r'^search/(?P<page>[0-9]+)/$', 'web.views.search'),
    url(r'^(?P<eid>[0-9]+)/$', 'web.views.detail'),
)
