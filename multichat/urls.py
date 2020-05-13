from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from chat.views import IndexView
from common import views

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    # path('accounts/login/', login, name='login'),
    path('accounts/login/user/', views.LoginView.as_view(), name='user_login'),
    path('accounts/login/user/<int:pk>/', views.UserProfileUpdateView.as_view(), name='profile_update'),
    path('accounts/logout/', logout),
    path('admin/', admin.site.urls),
    path("register/", views.RegisterView.as_view(), name="register"),
    path('chat/', include(('chat.urls', 'chat'), namespace='chat')),


]
