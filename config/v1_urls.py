from django.urls import path, include

app_name = 'v1'
urlpatterns = [
    path('ssa/', include('server_side_app.urls')),
]
