from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes


@api_view(['POST'])
@permission_classes([])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Authentification Django
    user = authenticate(username=username, password=password)
    
    if user is not None:
        if user.is_staff:  # On vérifie que c'est bien un admin
            login(request, user)
            return Response({'detail': 'Success'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Accès réservé aux administrateurs'}, status=status.HTTP_403_FORBIDDEN)
    
    return Response({'detail': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)