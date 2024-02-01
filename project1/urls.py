"""
URL configuration for project1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',views.home,name='home'),
    path('notes/',views.notes,name='notes'),
    path('delete_note/<int:pk>',views.Delete_note,name='delete_note'),
    # path('notes_detail/<int:pk>',views.NotesDetailsViews.as_view(),name='notes_detail'),
    path('notes_detail/<int:id>',views.NotesDetail,name='notes_detail'),

    path('homework/',views.Homework,name='homework'),
    path('delete_homework/<int:pk>',views.homework_Delete,name='delete_homework'),
    path('update_homework/<int:pk>',views.homework_update,name='update_homework'),

    path('youtube/',views.youtube,name='youtube'),

    path('todo/',views.Todos,name='todo'),
    path('update_todo/<int:pk>',views.update_todo,name='update_todo'),
    path('delete-todo/<int:pk>',views.Delete_todo,name='delete-todo'),

    path('book',views.books,name='book'),

    path('dict/',views.Dictionary,name='dict'),

    path('wiki/',views.Wiki,name='wiki'),

    path('conversion/',views.conversion,name='conversion'),

    path('',views.register,name='register'),

    path('login/',views.Login,name='login'),

    path('logout/', views.Logout, name='logout'),
    
    path('profile/',views.profile,name='profile')
]



# Student
# pavan123

