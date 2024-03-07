from datetime import date
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from rest_framework.response import Response
from rest_framework import status

import uuid

class UserManager(BaseUserManager):
    def create_user(self, nome, sobrenome, nasc, cpf, email, password, isgoogle, google_id = None) :
        if isgoogle == False:
            campos = ['nome', 'sobrenome', 'nasc', 'cpf', 'email', 'password','isgoogle']
        else:
            campos = ['nome', 'sobrenome', 'nasc', 'cpf', 'email','isgoogle','google_id']
           
        for i in campos:
            if i == False or not i:
                return Response({"Erro": f"O campo {i} não foi preenchido corretamente"}, status = status.HTTP_400_BAD_REQUEST)
        
        else:
            email = self.normalize_email(email)
            user = self.model(email = email, nome = nome, sobrenome = sobrenome, nasc = nasc, cpf = cpf, isgoogle = isgoogle, google_id = google_id)
            user.set_password(password)
            
            user.save() 
            return user
    
    
        
class Users(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key = True, unique = True, editable = False, default = uuid.uuid4, auto_created = True)
    nome = models.CharField(max_length = 30 , blank = False, null = False)
    sobrenome = models.CharField(max_length = 30 , blank = False, null = False)
    nasc = models.DateField(default = None, null = True)
    
    data_create = models.DateField(auto_created = True, default=date.today)
    cpf = models.CharField(max_length = 14, unique = True, blank = False, null = False)
    email = models.EmailField(max_length = 150, unique = True, blank = False, null = False)
    telefone = models.CharField(max_length = 11)
    isgoogle = models.BooleanField(default = False)
    google_id = models.CharField(default = None,max_length = 300, blank = True, null = True )
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'sobrenome', 'nasc', 'cpf']
    objects = UserManager()        



class Endereco(models.Model):
    id = models.UUIDField(primary_key = True, editable = False, unique = False, auto_created = True, default = uuid.uuid4)
    user = models.ForeignKey(Users, on_delete = models.CASCADE)
    cep = models.CharField(max_length = 8, blank = False, null = False)
    estado = models.CharField(max_length = 20, blank = False, null = False)
    cidade = models.CharField(max_length = 30, blank = False, null = False)
    bairro = models.CharField(max_length = 40, blank = False, null = False)
    rua = models.CharField(max_length = 30, blank = False, null = False)
    numero = models.SmallIntegerField(blank = False, null = False)
    complemento = models.CharField(max_length = 100, blank = True, null = True)
    
    
    


'''


164 329 924 78 
class Carrinho(models.Model):
    pass

class Lojas(AbstractBaseUser, PermissionsMixin):
    pass 

class Produtos(models.Model):
    pass

'''