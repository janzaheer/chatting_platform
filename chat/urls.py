from django.urls import path
from chat import views

urlpatterns = [
    path('room/create/', views.CreateRoomView.as_view(), name='create_room'),
    path('room/list/', views.Rooms.as_view(), name='room'),
    path('room/detail/<int:pk>/', views.RoomDetailView.as_view(),name='room_detail'),
    path('room/status/requeste/', views.MemberPAgeRequestAPIView.as_view(),
         name='member_room_request'
         ),
    path('room/chatting/', views.Rooms.as_view(), name='rooms'),
    path('owner/dashboard/', views.OwnerDashboard.as_view(), name='owner_dashboard'),
    path('room/owner/<int:pk>/create/admin/page/', 
    	views.CreatePageAdminView.as_view(),name='create_room_admin'),
    path('room/admin/dashboard/', views.AdminDashboardView.as_view(),
    	 name='admin_dashboard'),
    path('room/admin/dashboard/', views.MemberPageRequestApproveAPIView.as_view(),
    	 name='member_request_approve'),
	path('public/', views.PublicDiscussion.as_view(), name='public_discuss'),
	path('room/<int:room_id>/user/<int:user_id>/request', views.JoinRequest.as_view(), name='room_request'),
]
