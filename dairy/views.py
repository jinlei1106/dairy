from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import list_route, detail_route

from .models import Daily
from .filters import DairyFilter
from .serializers import DariyListSerializer
from apps.operate.models import Approval, Comment


class DairyViewSet(viewsets.ModelViewSet):
    queryset = Daily.objects.filter(share=True)
    serializer_class = DariyListSerializer
    filter_class = DairyFilter
    permission_classes = (IsAuthenticated,)

    @list_route()
    def mine(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route()
    def approval(self, request, pk=None, *args, **kwargs):
        dairy = Daily.objects.get(id=pk)
        if not Approval.objects.filter(user=request.user, dairy=dairy).exists():
            approval = Approval(user=request.user, dairy=dairy)
            approval.save()
        else:
            Approval.objects.filter(user=request.user, dairy=dairy).delete()
        return Response({'message': '操作成功'}, status=status.HTTP_200_OK)

    @detail_route(methods=('post',))
    def comment(self, request, pk=None, *args, **kwargs):
        content = request.data.get('content', '')
        if not content:
            return Response({'message': '请填写内容'}, status=status.HTTP_400_BAD_REQUEST)
        dairy = Daily.objects.get(id=pk)
        comment = Comment(user=request.user, dairy=dairy, content=content)
        comment.save()
        return Response({'message': '操作成功'}, status=status.HTTP_200_OK)
