from django.urls import path
from ticketing_api import views
from django.conf.urls import url

urlpatterns = [
    url('getOrders/(?P<user_id>[0-9]*)', views.getOrders),
    url('users/', views.get_users),
    url('update-user', views.update_user),
]
