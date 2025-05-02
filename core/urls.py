from django.urls import path
from .views import home, about,test, contact, detail, location,login_view,register_view,logout_view
from . import views
from .views import post_edit 


app_name = 'core'

urlpatterns = [
   
    path('', views.home, name='home'),
    path('about/',about, name='about'),
    path('contact/', views.contact, name='contact'), 
    path('test/',test, name='test'),
    path('detail/<int:id>/',detail, name='detail'), 
    path('location/',location, name='location'),
    path('login/', login_view, name='login'), 
    path('register/',register_view,name='register'),
    path('logout/', logout_view, name='logout'),
    path('post_list/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('create/', views.post_create, name='post_create'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('increaselikes/<int:id>/', views.increaselikes, name='increaselikes'),
   

]
















  

