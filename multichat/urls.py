from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from chat.views import IndexView
from common import views
from django.conf.urls.static import static
from django.conf import settings

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


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
