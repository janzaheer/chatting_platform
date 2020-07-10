from django.views.generic import View
from django.http import JsonResponse,HttpResponse
from django.core import serializers

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
				'last_namt': user.last_name,
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
