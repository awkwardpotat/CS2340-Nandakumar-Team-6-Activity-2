from django.urls import path
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('login/', views.login, name='accounts.login'),
    path('signup/', views.signup, name='accounts.signup'),
    path('logout/', views.logout, name='accounts.logout'),
]