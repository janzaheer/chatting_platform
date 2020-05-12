from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView, DeleteView,FormView, ListView, UpdateView
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import forms as auth_forms
from django.db import transaction
from django.http import Http404
from django.db.models import Sum
from .models import UserProfile

class RegisterView(FormView):
    form_class = auth_forms.UserCreationForm
    template_name = 'registration/register.html'
    def form_valid(self, form):
        with transaction.atomic():
            user = form.save()
            user_profile = UserProfile.objects.get(user=user)
            user_profile.type = UserProfile.USER_TYPE_MEMBER
            user_profile.save()
            return HttpResponseRedirect(reverse('index'))

    def form_invalid(self, form):

        return super(RegisterView, self).form_invalid(form)