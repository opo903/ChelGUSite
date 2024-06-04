from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index_headman'),
    path('logout/', views.logout_view, name='logout_headman'),
    path('options/', views.options, name='options_headman'),
    path('save_attendance/', views.save_attendance, name='save_attendance'),
    path('add_student/', views.add_student, name='add_student'),
    path('del_student/', views.del_student, name='del_student'),
    path('update_account/', views.update_account, name='update_account_headman'),
]