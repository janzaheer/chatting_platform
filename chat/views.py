from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room, RoomAdmin, PublicRoom
from django.views.generic import View, DeleteView, ListView, FormView, UpdateView, TemplateView
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from common.models import MemberChatRoom, UserProfile
from django.contrib.auth.models import User
from django.http import Http404
from .forms import RoomAdminForm, RoomForm, CommentForm
from django.db import transaction
from common.models import UserProfile
from chat.models import Comment
from common.views import get_all_logged_in_users, logged_in_user_ids


class OwnerDashboard(TemplateView):
    template_name = 'rooms/owner_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(
            OwnerDashboard, self).get_context_data(**kwargs)
        rooms = Room.objects.all()
        members = User.objects.all()
        roomadmins = RoomAdmin.objects.filter(
            user__id=self.request.user.id)
        context.update({
            'rooms': rooms,
            'roomadmins': roomadmins,
            'members': members,
            'total_logged_in_users': get_all_logged_in_users().count(),
            'logged_in_members': get_all_logged_in_users(),

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

class CreateRoomView(FormView):
    form_class = RoomForm
    template_name = "rooms/create_room.html"

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('user_login'))
        return super(
            CreateRoomView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            room = form.save()

            room_admin_form_kwargs = {
                'room': room.id,
                'user': self.request.user.id
            }

            room_admin_form = RoomAdminForm(room_admin_form_kwargs)
            room_admin_form.save()

            return HttpResponseRedirect(reverse('chat:owner_dashboard'))

    def form_invalid(self, form):
        return super(CreateRoomView, self).form_invalid(form)


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

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(RoomDetailView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('user_login'))


    def get_context_data(self, **kwargs):
        context = super(
            RoomDetailView, self).get_context_data(**kwargs)
        try:
            room_detail = MemberChatRoom.objects.get(
                room__id=self.kwargs.get('pk')
            )
        except :
            room_detail = 'Cancel'
        room = Room.objects.get(id=self.kwargs.get('pk'))
        try:
            current_location_attending = room.room_member_chat_room.first().user.filter(
                id__in=logged_in_user_ids()).count()
            online_members = room_detail.user.filter(
                id__in=logged_in_user_ids())
        except:
            current_location_attending = 0
            online_members = []


        context.update({
            'room': room,
            'room_detail':room_detail,
            'total_logged_in_users': get_all_logged_in_users().count(),
            'current_location_attending': current_location_attending,
            'online_members': online_members,
            'logged_in_members': get_all_logged_in_users(),

        })
        return context

class IndexView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('user_login'))

        if (
                    self.request.user.user_profile.type ==
                    self.request.user.user_profile.USER_TYPE_PAGE_ADMIN
        ):

            return HttpResponseRedirect(reverse('chat:owner_dashboard'))
        else:
            return HttpResponseRedirect(reverse("chat:rooms"))


    def get_context_data(self, **kwargs):
        context = super(
            IndexView, self).get_context_data(**kwargs)
        public_room = PublicRoom.objects.all()
        context.update({
            'room': public_room,
            'logged_in_users': get_all_logged_in_users(),

        })
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


class PublicDiscussion(FormView):
    template_name = 'public_discussion.html'
    form_class = CommentForm

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('chat:public_discuss'))
    
    def form_invalid(self, form):
        return super(PublicDiscussion, self).form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(
                PublicDiscussion, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('user_login'))

    def get_context_data(self, **kwargs):
        context = super(PublicDiscussion, self).get_context_data(**kwargs)
        comments = Comment.objects.all()
        context.update({
            'comments': comments,
            'total_logged_in_users': get_all_logged_in_users().count(),
            'logged_in_members': get_all_logged_in_users(),
        })
        return context


class Rooms(TemplateView):
    template_name = 'rooms/chating_room.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('user_login'))
        return super(Rooms, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Rooms, self).get_context_data(**kwargs)
        context.update({
            'total_logged_in_users': get_all_logged_in_users().count(),
            'logged_in_members': get_all_logged_in_users(),
            'rooms': Room.objects.all().order_by('-id')
        })
        return context


class JoinRequest(View):
    def get(self, request, *args, **kwargs):
        MemberChatRoom.objects.create(
            user=User.objects.get(id=self.kwargs.get('user_id')),
            room=Room.objects.get(id=self.kwargs.get('room_id')),
            status=MemberChatRoom.CHAT_TYPE_REQUESTED,
        )
        return HttpResponseRedirect(reverse('chat:rooms'))
