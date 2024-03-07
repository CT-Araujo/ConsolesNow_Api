from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .validators import ValidaSenha, get_tokens_for_user, ValidaCep

from .serializers import UserSerializer, Usermodel, EnderecoSerializers, UsersLoginSerializer
from .models import Endereco


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
            
            if ValidaSenha(senha).status_code == 200:
                
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
            return Response(ValidaSenha(senha).data, status = status.HTTP_400_BAD_REQUEST) # Caso a senha esteja invalida
        return Response(serialzers.errors,status = status.HTTP_400_BAD_REQUEST) # Caso os dados do serializers não seja válido
    
    
    def delete(self, request):
        filtro = request.query_params.get('id', None)
        user = Usermodel.objects.get(id = filtro)
        if user:
            user.delete()
            return Response(status = status.HTTP_200_OK)
        



class UsersLoginViews(APIView):
    def post(self,request):
        serializers = UsersLoginSerializer(data = request.data)
        
        if serializers.is_valid():
            user = authenticate(username = serializers.validated_data['email'], password = serializers.validated_data['password'])
            user_data = Usermodel.objects.get(email = serializers.validated_data['email'])
            if user:
                token = get_tokens_for_user(user)
                if token:
                    dados = {
                        "Token": token,
                        "id": user_data.id
                        
                    }
                    return Response(dados, status = status.HTTP_200_OK)
                return Response({"Message":"Erro na geração do token"}, status = status.HTTP_401_UNAUTHORIZED)
            return Response({"Message":"Usuário não autenticado"}, status = status.HTTP_201_CREATED)



class EnderecoViews(APIView):
    def get(self, request):
        dados = Endereco.objects.all()
        serialzed = EnderecoSerializers(dados, many = True)
        
        return Response(serialzed.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        serializer = EnderecoSerializers(data = request.data)
        
        if serializer.is_valid():
            cep =  ValidaCep(serializer.validated_data['cep'])
            if cep.status_code == 200:
                if Endereco.objects.filter(user = serializer.validated_data['user']).count() < 2:
                    
                    new_endereco  = Endereco.objects.create(
                        user = serializer.validated_data['user'],
                        cep = serializer.validated_data['cep'],
                        estado = serializer.validated_data['estado'],
                        cidade = serializer.validated_data['cidade'],
                        bairro = serializer.validated_data['bairro'],
                        rua = serializer.validated_data['rua'],
                        numero = serializer.validated_data['numero'],
                        complemento = serializer.validated_data['complemento'],
                        
                    )
                    
                    new_endereco.save()
                    new_endereco_serialized = EnderecoSerializers(new_endereco)
                    
                    return Response(new_endereco_serialized.data, status = status.HTTP_201_CREATED)
            
                return Response({'Message':"Já existem dois endereços relacionado a esse usuário"}, status = status.HTTP_400_BAD_REQUEST)
            return Response(cep.data)
        return Response({"Message":"Dados inválidos."}, status = status.HTTP_400_BAD_REQUEST)
    
    
    def patch(self, request):
        if request.method == 'PATCH':
            filtro = request.query_params.get('id', None)
            existe = Endereco.objects.filter(id = filtro).exists()
        
            if existe:
                produto = Endereco.objects.get(id = filtro)
                serializer = EnderecoSerializers(produto, data= request.data, partial = True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status= status.HTTP_200_OK)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response({"Message":"Endereço não encontrado"},status=status.HTTP_404_NOT_FOUND)
        
    
    
    def get_permissions(self):

        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAuthenticated()]
        return super().get_permissions()