from django.views.generic import View
from django.http import JsonResponse,HttpResponse
from django.core import serializers
from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from common.views import get_all_logged_in_users


class LoggedInUserAPI(View):
	def get(self, request, *args, **kwargs):
		users = get_all_logged_in_users()
		data = []
		for user in users:
			user = {
				'id': user.id,
				'username': user.username,
				'first_name': user.first_name,
				'last_name': user.last_name,
				'email': user.email,
				'status': user.user_profile.status,
				'linked_in': user.user_profile.linked_in or '',
				'facebook': user.user_profile.facebook or '',
				'youtube': user.user_profile.youtube or '',
				'google_plus': user.user_profile.google_plus or '',
			}
			data.append(user)

		response = JsonResponse({
			'users': data,
			'total_user': users.count()
		})
		response["Access-Control-Allow-Origin"] = "*"
		response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
		response["Access-Control-Max-Age"] = "1000"
		response[
			"Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
		return response


class UpdateUserStatusAPI(View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(UpdateUserStatusAPI, self).dispatch(request, *args, *kwargs)

	def post(self, request, *args, **kwargs):

		from rest_framework.authtoken.models import Token
		if self.request.META.get('HTTP_TOKEN'):
			try:
				token = Token.objects.get(key=self.request.META.get('HTTP_TOKEN'))
			except:
				response = JsonResponse({
					'message': 'Invalid User'
				})
				response["Access-Control-Allow-Origin"] = "*"
				response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
				response["Access-Control-Max-Age"] = "1000"
				response[
					"Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
				return response
		else:
			response = JsonResponse({
				'message': 'Token is required'
			})
			response["Access-Control-Allow-Origin"] = "*"
			response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
			response["Access-Control-Max-Age"] = "1000"
			response[
				"Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
			return response



		user = token.user
		user.user_profile.status = self.request.POST.get('status')
		user.user_profile.save(update_fields=['status'])

		response =  JsonResponse({
			'user_status': user.user_profile.status,
			'message': 'Success'
		})

		response["Access-Control-Allow-Origin"] = "*"
		response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
		response["Access-Control-Max-Age"] = "1000"
		response[
			"Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
		return response
