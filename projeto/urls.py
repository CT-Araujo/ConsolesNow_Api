
from django.contrib import admin
from django.urls import path
from app.views import UsersViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',UsersViews.as_view(), name = 'usuarios')
]
