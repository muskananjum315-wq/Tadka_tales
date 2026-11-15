from django.urls import path
from . import views
from .views import toggle_favourite, my_favourites

urlpatterns = [
    path('',views.home,name='home'),
    path('menu/', views.menu, name='menu'),
    path('region/', views.region, name='region'),
    path('all_dishes/',views.all_dishes,name='all_dishes'),
    path('dish/<str:dish_name>/',views.dish_detail,name='dish_detail'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('restaurants/',views.restaurants,name='restaurants'),
    path('restaurant/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path(
    'favourite/<int:dish_id>/',
    views.toggle_favourite,
    name='toggle_favourite'
),
path(
    'my-favourites/',
    views.my_favourites,
    name='my_favourites'
),
   
]