from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from chat.views import IndexView
from common import views
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.routers import DefaultRouter
from common.api import MessageModelViewSet, UserModelViewSet

router = DefaultRouter()
router.register(r'message', MessageModelViewSet, basename='message-api')
router.register(r'user', UserModelViewSet, basename='user-api')


urlpatterns = [
    path(r'chat/api/v1/', include(router.urls)),
    path('', IndexView.as_view(), name="index"),
    path('chat/single', views.SingleChatView.as_view(), name="single_chat"),
    # path('accounts/login/', login, name='login'),
    path('accounts/login/user/', views.LoginView.as_view(), name='user_login'),
    path('accounts/login/user/<int:pk>/', views.UserProfileUpdateView.as_view(), name='profile_update'),
    path('accounts/logout/', logout),
    path('admin/', admin.site.urls),
    path("register/", views.RegisterView.as_view(), name="register"),
    path('chat/', include(('chat.urls', 'chat'), namespace='chat')),
    path('user/<int:user_id>/update', views.UpdateStatusAPI.as_view(), name="update_status_api"),

]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
