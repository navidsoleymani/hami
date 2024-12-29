from django.urls import path
from .views import add_goal, get_user_goals, all_goals, delete_goal

urlpatterns = [
    path('add-goal/', add_goal),
    path('delete-goal/', delete_goal),
    path('get-goals/', get_user_goals),
    path('get-all-goals/', all_goals),
]
