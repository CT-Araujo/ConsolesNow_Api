from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .validators import Valida_senha, get_tokens_for_user

from .serializers import UserSerializer, Usermodel

class UsersViews(APIView):
    def get(self, request):
        dados = Usermodel.objects.all()
        serializers = UserSerializer(dados, many = True)
        
        return Response(serializers.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        serialzers = UserSerializer(data = request.data)
        
        if serialzers.is_valid():
            
            email = serialzers.validated_data.get('email')
            senha = serialzers.validated_data.get('password')
            
            if Valida_senha(senha).status_code == 200:
                
                user = serialzers.create(serialzers.validated_data)
                autentica = authenticate(username = email, password = senha)
                
                user_data = Usermodel.objects.get(email = email)
                if autentica:
                    token = get_tokens_for_user(autentica)
                    
                    if token:
                        
                        dados = {
                            "Id": user_data.id,
                            "Email": email, 
                            "Token": token
                        }
                        
                        return Response(dados, status = status.HTTP_201_CREATED)
                    
                    return Response({"Message":"Erro na geração do token"}, status = status.HTTP_401_UNAUTHORIZED) #Caso o token não seja gerado corretamente
                return Response({"Message":"Erro na autenticação"}, status = status.HTTP_401_UNAUTHORIZED) # Caso o usuário não seja autenticado
            return Response(Valida_senha(senha).data, status = status.HTTP_400_BAD_REQUEST) # Caso a senha esteja invalida
        return Response(serialzers.errors,status = status.HTTP_400_BAD_REQUEST) # Caso os dados do serializers não seja válido
    
    
    def delete(self, request):
        filtro = request.query_params.get('id', None)
        user = Usermodel.objects.get(id = filtro)
        if user:
            user.delete()
            return Response(status = status.HTTP_200_OK)
        