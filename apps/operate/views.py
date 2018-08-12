from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import list_route

from .models import Approval, Comment
from dairy.serializers import DairyListSerializer
from dairy.models import Daily


class OperateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Daily.objects.all()
    serializer_class = DairyListSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_403_FORBIDDEN)

    @list_route(methods=('get',))
    def approved(self, request):
        queryset = []
        qs = Approval.objects.filter(user=request.user)
        for q in qs:
            queryset.append(q.dairy)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=('get',))
    def commented(self, request):
        queryset = []
        qs = Comment.objects.filter(user=request.user)
        for q in qs:
            queryset.append(q.dairy)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)