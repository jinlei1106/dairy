from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import list_route

from .models import Approval, Comment
from dairy.serializers import DariyListSerializer


class OperateViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @list_route(methods=('get',))
    def approved(self, request):
        queryset = []
        qs = Approval.objects.filter(user=request.user)
        for q in qs:
            queryset.append(q.dairy)
        serializer = DariyListSerializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=('get',))
    def commented(self, request):
        queryset = []
        qs = Comment.objects.filter(user=request.user)
        for q in qs:
            queryset.append(q.dairy)
        serializer = DariyListSerializer(queryset, many=True)
        return Response(serializer.data)