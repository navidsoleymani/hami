import contextlib
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import serializers

from .models import FollowerCount, Goal


class FollowerCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowerCount
        fields = "__all__"


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = "__all__"


@require_http_methods(['GET'])
def add_goal(request):
    with contextlib.suppress(Exception):
        t_id = request.GET.get('t_id')
        instagram_id = request.GET.get('instagram_id')
        follower_count = request.GET.get('follower_count')
        goal = Goal()
        goal.user_id = instagram_id
        goal.follower_count = follower_count
        goal.telegram_user = t_id
        goal.save()
        return JsonResponse(GoalSerializer(goal).data)
    return JsonResponse({}, status=500)


@require_http_methods(['GET'])
def delete_goal(request):
    with contextlib.suppress(Exception):
        goal_id = request.GET.get('goal_id')
        Goal.objects.get(id=goal_id).delete()
        return JsonResponse({}, status=200)
    return JsonResponse({}, status=500)


@require_http_methods(['GET'])
def all_goals(request):
    with contextlib.suppress(Exception):
        goals = Goal.objects.all()
        return JsonResponse(GoalSerializer(goals, many=True).data, safe=False)
    return JsonResponse({}, status=500)


@require_http_methods(['GET'])
def get_user_goals(request):
    with contextlib.suppress(Exception):
        t_id = request.GET.get('t_id')
        goals = Goal.objects.filter(telegram_user=t_id).all()
        return JsonResponse(GoalSerializer(goals, many=True).data, safe=False)
    return JsonResponse({}, status=500)
