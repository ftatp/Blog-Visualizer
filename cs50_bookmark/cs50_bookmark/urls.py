"""cs50_bookmark URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from bookmark import views

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'^$', views.index, name="index"),
    url(r'test_index', views.test_index, name="test_index"),
    url(r'(?P<user_name>[A-Za-z]+)/$', views.hello, name="hello_user"),
    url(r'^bookmark$', views.bookmark, name="bookmark"),
    url(r'^login$', views.login, name="login"),
    url(r'^login_check$', views.login_check, name="login_check"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^logout_process$', views.logout_process, name="logout_process"),
    url(r'^user_registeration', views.user_registeration, name="user_registeration"),
    url(r'^bookmark_list', views.bookmark_list, name="bookmark_list"),
    url(r'^bookmark_detail/(?P<id>[0-9]+)$', views.bookmark_detail, name='bookmark_detail'),
    url(r'^post_comment$', views.post_comment, name='post_comment')
    #url(r'template_tester', views.new_time, name="index_1")
]
