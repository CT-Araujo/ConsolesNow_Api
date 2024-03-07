from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import requests 

def ValidaSenha(senha):
    if len(str(senha)) < 8:
        return Response({"Message": "Senha muito curta, é necessário que possua mais de 8 caracteres"})
    else:
        def has_special_character():
            for esp in senha:
                if not esp.isalnum() and esp.isascii():
                    return True
            return False

        def has_alphanumeric():
            for l in senha:
                if l.isalnum():
                    return True
            return False

        if not has_special_character() or not has_alphanumeric():
            return Response({"Message": "Senha inválida, deve conter caracteres especiais e alfanuméricos."}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(senha, status = status.HTTP_200_OK)
        
        
def ValidaCep(cep):
    if len(str(cep)) < 8:
        return Response({"Message":"CEP inválido, informe um CEP com 8 digitos numericos"}, status = status.HTTP_400_BAD_REQUEST)
    
    url = "https://viacep.com.br/ws/01001000/json/"
    
    response = requests.get(url)
    
    if 'erro' in response.json():
        return Response({"Message":"O CEP informado não corresponde a nenhuma localidade."}, status = status.HTTP_400_BAD_REQUEST)
    
    return Response(response.text, status = status.HTTP_200_OK)
   


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
    }