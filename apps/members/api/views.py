from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Q
from ..models import Member
from .serializers import MemberSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAdminUser]

    # Cette action crée l'endpoint : /api/members/search/
    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        query = request.query_params.get('q', '')
        if query:
            members = Member.objects.filter(
                Q(full_name__icontains=query) | 
                Q(phone__icontains=query)
            )[:10] # On limite à 10 résultats pour la performance
        else:
            members = Member.objects.none()
            
        serializer = self.get_serializer(members, many=True)
        return Response(serializer.data)