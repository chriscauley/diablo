from django.conf.urls.defaults import *

urlpatterns = patterns(
    'diablo.views',
    url(r'^account/(\d+)/$','account_detail',name='diablo_account_detail'),
    url(r'^hero/(\d+)/$','hero_detail',name='diablo_hero_detail'),
    url(r'^add/$','add_account',name='diablo_add_account'),
    url(r'^edit/(\d+)/$','edit_account',name='diablo_edit_account'),
    )
