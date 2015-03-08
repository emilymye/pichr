from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^search/', 'pichr.views.search'),
    url(r'^$', 'pichr.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
)
