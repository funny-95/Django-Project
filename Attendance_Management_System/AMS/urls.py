from django.conf.urls import url
from AMS import views

urlpatterns = [
    url(r'^$', views.index, name='homepage'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^write_note/$', views.write_note, name='write_note'),
    url(r'^view_note/$', views.view_note, name='view_note'),
    url(r'^set_password/$', views.set_password, name='set_password'),
    url(r'^view_file_list/$', views.view_file_list, name='view_file_list'),
    url(r'^view_book/detail/$', views.detail, name='detail'),
    url(r'^qiandao/$',views.qiandao,name = 'qiandao'),

    url(r'^user_manage/$',views.user_manage,name = 'user_manage'),
    url(r'^user_manage/add_user/$',views.add_user,name = 'add_user'),
    url(r'^user_manage/modify_user/$',views.modify_user,name = 'modify_user'),
    url(r'^user_manage/delete_user/$',views.delete_user,name = 'delete_user'),

    url(r'^qingjia_manage/$',views.qingjia_manage,name = 'qingjia_manage'),
    url(r'^shenpi_qingjia/$',views.shenpi_qingjia,name = 'shenpi_qingjia'),

    url(r'^salary_manage/$',views.salary_manage,name = 'salary_manage'),
    url(r'^salary_manage/base_salary/$',views.base_salary,name = 'base_salary'),
    url(r'^salary_manage/salary_detail/$',views.salary_detail,name = 'salary_detail'),

    url(r'^comment_manage/$',views.comment_manage,name = 'comment_manage'),
    url(r'^comment_manage/add_comment/$',views.add_comment,name = 'add_comment'),
    url(r'^comment_manage/modify_comment/$',views.modify_comment,name = 'modify_comment'),
    url(r'^comment_manage/delete_comment/$',views.delete_comment,name = 'delete_comment'),
]