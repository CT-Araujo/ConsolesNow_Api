
from django.contrib import admin
from django.urls import path
from app.views import UsersViews, EnderecoViews, UsersLoginViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',UsersViews.as_view(), name = 'usuarios'),
    path('endereco/',EnderecoViews.as_view(), name = 'endereco'),
    path('login/', UsersLoginViews.as_view(), name = 'login'),
]
