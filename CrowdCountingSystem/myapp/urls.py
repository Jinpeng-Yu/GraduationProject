from django.conf.urls import url, include
from . import views

# 正在部署的应用名称
app_name = 'counting'

urlpatterns = [
    url(r'login$', views.login),
    url(r'add_manager$', views.add_manager, ),
    url(r'delete_manager$', views.delete_manager, ),
    url(r'update_manager$', views.update_manager, ),
    url(r'show_managers$', views.show_managers, ),
    url(r'get_user_by_id$', views.get_user_by_id, ),
    url(r'update_manager_state$', views.update_manager_state),
    url(r'upload_video$', views.upload_video),
    url(r'analyse_video', views.analyse_video),
    url(r'data_visual', views.data_visual),
]