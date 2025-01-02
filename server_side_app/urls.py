from django.urls import path
from .views import add_goal, get_user_goals, all_goals, delete_goal

urlpatterns = [
    path('goals/add/', add_goal),
    path('goals/delete/<uuid:goal_id>/', delete_goal),
    path('goals/getlist/', all_goals),
    path('goals/getlist/<str:t_id>/', get_user_goals),
]
