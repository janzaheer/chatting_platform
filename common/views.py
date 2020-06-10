from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView, DeleteView,FormView, ListView, UpdateView
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import forms as auth_forms
from django.db import transaction
from django.http import Http404
from django.db.models import Sum
from django.contrib.auth import login as auth_login
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone


def get_all_logged_in_users():
	# Query all non-expired sessions
	# use timezone.now() instead of datetime.now() in latest versions of Django
	sessions = Session.objects.filter(expire_date__gte=timezone.now())
	uid_list = []

	# Build a list of user ids from that query
	for session in sessions:
		data = session.get_decoded()
		uid_list.append(data.get('_auth_user_id', None))

	# Query all logged in users based on id list
	return User.objects.filter(id__in=uid_list)


def logged_in_user_ids():
	# Query all non-expired sessions
	# use timezone.now() instead of datetime.now() in latest versions of Django
	sessions = Session.objects.filter(expire_date__gte=timezone.now())
	uid_list = []

	# Build a list of user ids from that query
	for session in sessions:
		data = session.get_decoded()
		uid_list.append(data.get('_auth_user_id', None))

	return uid_list


class LoginView(FormView):
	template_name = 'registration/login.html'
	form_class = auth_forms.AuthenticationForm

	def dispatch(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			if (
						self.request.user.user_profile.type ==
						self.request.user.user_profile.USER_TYPE_PAGE_ADMIN
			):
				print("______________________o____________-")
				return HttpResponseRedirect(reverse('chat:owner_dashboard'))
			elif (
						self.request.user.user_profile.type ==
						self.request.user.user_profile.USER_TYPE_USER
			):
				print("______________________o____________-")

				return HttpResponseRedirect(reverse("index"))
			elif (
						self.request.user.user_profile.type ==
						self.request.user.user_profile.USER_TYPE_MEMBER
			):
				print("______________________o____________-")

				return HttpResponseRedirect(reverse("chat:rooms"))
			elif (
						self.request.user.user_profile.type ==
						self.request.user.user_profile.USER_TYPE_PAGE_ADMIN
			):
				print("______________________o____________-")

				return HttpResponseRedirect(reverse("index"))

		return super(LoginView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		user = form.get_user()
		auth_login(self.request, user)
		print("________________________________")
		if (
					self.request.user.user_profile.type ==
					self.request.user.user_profile.USER_TYPE_PAGE_ADMIN
		):
			print("______________________o____________-")
			return HttpResponseRedirect(reverse('chat:owner_dashboard'))
		else:
			return HttpResponseRedirect(reverse('chat:rooms'))

	def form_invalid(self, form):
		return super(LoginView, self).form_invalid(form)


class RegisterView(FormView):
	form_class = auth_forms.UserCreationForm
	template_name = 'registration/register.html'
	def form_valid(self, form):
		with transaction.atomic():
			user = form.save()
			user_profile = UserProfile.objects.get(user=user)
			user_profile.phone=self.request.POST.get('phone')
			user_profile.email=self.request.POST.get('emial')
			user_profile.company_name=self.request.POST.get('company')
			user_profile.type = UserProfile.USER_TYPE_USER
			user_profile.save()
			return HttpResponseRedirect(reverse('index'))

	def form_invalid(self, form):

		return super(RegisterView, self).form_invalid(form)

class UserProfileUpdateView(UpdateView):
	model = UserProfile
	form_class = UserProfileForm
	template_name = 'registration/update_profile.html'

	def dispatch(self, request, *args, **kwargs):
		if not self.request.user.is_authenticated:
			return HttpResponseRedirect(reverse('login'))
		return super(
			UserProfileUpdateView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		obj=form.save()
		return HttpResponseRedirect(
			reverse('chat:room_detail', kwargs={'pk': 2}))

	def form_invalid(self, form):
		print(form.errors)
		print("_________________________")
		return super(UserProfileUpdateView, self).form_invalid(form)

	def get_context_data(self, **kwargs):
		context = super(UserProfileUpdateView, self).get_context_data(**kwargs)
		context.update({
			'total_logged_in_users': get_all_logged_in_users().count() - 1,
		})
		return context

