from rest_framework import serializers
from rest_framework import status
from django.contrib.auth import get_user_model
Usermodel = get_user_model()
from .models import Endereco

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only = True)
    
    class Meta:
        model = Usermodel
        fields = ['nome', 'sobrenome', 'nasc', 'cpf', 'email', 'password','confirm_password','isgoogle','google_id']
        extra_kwargs = {
            'password': {'write_only': True},
            }
        
    def validate(self, data):
        if data.get('confirm_password') != data.get('password'):
            raise serializers.ValidationError("As senhas não coincidem.")
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        
        isgoogle = validated_data.get('user_google', False)
        
        google_id = validated_data.get('google_id', None)
        
        nasc = validated_data.get('nasc', None)
        user = Usermodel.objects.create_user(
            nome = validated_data['nome'],
            sobrenome = validated_data['sobrenome'], 
            nasc = nasc,
            cpf = validated_data['cpf'], 
            email = validated_data['email'], 
            password  = validated_data['password'],  
            isgoogle = isgoogle, 
            google_id = google_id)
        
        user.save()
        return user
    
class UsersLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    
    
class EnderecoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'
        