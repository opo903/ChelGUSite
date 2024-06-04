from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index_teacher'),
    path('logout/', views.logout_view, name='logout_teacher'),
    path('options/', views.options, name='options_teacher'),
    path('update_account/', views.update_account, name='update_account_teacher'),
    path('subgroups_select/<int:key_group>/', views.subgroups_select, name='subgroups_select_teacher'),
    path('table_students/<int:key_subgroup>/', views.table_students, name='table_students_teacher'),
    path('search_students_teacher/', views.search_students_teacher, name='search_students_teacher'),
]