from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room, RoomAdmin
from django.views.generic import View, DeleteView, ListView, FormView, UpdateView, TemplateView
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from common.models import MemberChatRoom, UserProfile
from django.contrib.auth.models import User
from django.http import Http404
from .forms import RoomAdminForm
from django.db import transaction
from common.models import UserProfile


class OwnerDashboard(TemplateView):
    template_name = 'rooms/owner_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(
            OwnerDashboard, self).get_context_data(**kwargs)
        rooms = Room.objects.all()
        members = User.objects.all()
        context.update({
            'rooms': rooms,
            'members': members

        })
        return context


class CreatePageAdminView(FormView):
    form_class = RoomAdminForm
    template_name = "rooms/create_page_admin.html"

    def form_valid(self, form):
        with transaction.atomic():
            print(self.request.POST.get('room'))
            print("________________________________________")
            obj=form.save()
            user_profile = UserProfile.objects.get(user=obj.user)
            user_profile.type = 'page_admin'
            user_profile.save()
            return HttpResponseRedirect(reverse('chat:owner_dashboard'))

    def form_invalid(self, form):
        return super(CreatePageAdminView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(
            CreatePageAdminView, self).get_context_data(**kwargs)
        room = Room.objects.get(id=self.kwargs.get('pk'))
        user = User.objects.all()
        room_admins = RoomAdmin.objects.all()
        context.update({
            'room': room,
            'users':user,
            'room_admins': room_admins

        })
        return context

class Rooms(TemplateView):
    template_name = 'rooms/rooms.html'

    def get_context_data(self, **kwargs):
        context = super(
            Rooms, self).get_context_data(**kwargs)
        rooms = Room.objects.all()
        context.update({
            'rooms': rooms,

        })
        return context

class RoomDetailView(TemplateView):
    template_name = 'rooms/room_detail.html'

    def get_context_data(self, **kwargs):
        context = super(
            RoomDetailView, self).get_context_data(**kwargs)
        try:
            room_detail = MemberChatRoom.objects.get(
                room__id=self.kwargs.get('pk')
            )
        except :
            room_detail = 'cancle'
        room = Room.objects.get(id=self.kwargs.get('pk'))
        context.update({
            'room': room,
            'room_detail':room_detail

        })
        return context

class IndexView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):

        if self.request.user.is_authenticated:
            if (
                self.request.user.user_profile.type ==
                self.request.user.user_profile.USER_TYPE_OWNER
            ):
                return HttpResponseRedirect(reverse('chat:owner_dashboard'))

    def get_context_data(self, **kwargs):
        context = super(index, self).get_context_data(**kwargs)
        return context

# @login_required
# def index(request):
#     print("_________________________")

#     def dispatch(self, request, *args, **kwargs):
#         print("___________FFF_________________")

#         if self.request.user.is_authenticated:
#            if(
#                self.request.user.user_profile.type ==
#                 self.request.user.user_profile.USER_TYPE_OWNER
#            ):
#                return HttpResponseRedirect(reverse("chat:owner_dashboard"))
#            else:
#                return HttpResponseRedirect(reverse("login"))

#         return super(index, self).dispatch(request, *args, **kwargs)
#     rooms = Room.objects.order_by("title")

#     # Render that in the index template
#     return render(request, "index.html", {
#         "rooms": rooms,
#     })

class MemberPAgeRequestAPIView(View):
    def post(self, request, *args, **kwargs):
        print('coming______________________')
        u_id=self.request.POST.get('user_id')
        r_id=self.request.POST.get('room_id')
        users = User.objects.filter(id=u_id)
        rooms = Room.objects.filter(id=r_id)
        instance = MemberChatRoom.objects.create(status='requested')

        for user in users:
            instance.user.add(user)
        for room in rooms:
            instance.room.add(room)

        status = instance.status
        return JsonResponse({
            'status': status,
        })


class ChattingRooms(TemplateView):
    template_name = 'rooms/chating_room.html'

    def get_context_data(self, **kwargs):
        context = super(
            ChattingRooms, self).get_context_data(**kwargs)
        rooms = Room.objects.all()
        context.update({
            'rooms': rooms,

        })
        return context

class AdminDashboardView(TemplateView):
    template_name = 'rooms/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(
            AdminDashboardView, self).get_context_data(**kwargs)
        rooms = MemberChatRoom.objects.get(user__id=self.request.user.id)
        context.update({
            'room_detail': rooms,

        })
        return context


class MemberPageRequestApproveAPIView(View):
    def post(self, request, *args, **kwargs):
        print('coming______________________')
        u_id=self.request.POST.get('user_id')
        print(u_id)
        print("_____________________________")
        room_member = MemberChatRoom.pobjects.get(user__id=u_id)
        room_member.status= 'approved'
        room_member.save()
        return JsonResponse({
            'status': status,
        })