from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import list_route, detail_route

from .models import Daily
from .filters import DairyFilter
from .serializers import DairyListSerializer, ApprovedUserSerializer, CommentSerializer
from apps.operate.models import Approval, Comment


class DairyViewSet(viewsets.ModelViewSet):
    queryset = Daily.objects.filter(share=True)
    serializer_class = DairyListSerializer
    filter_class = DairyFilter
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(share=True)
        return queryset

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
        try:
            dairy = Daily.objects.get(id=pk)
        except Daily.DoesNotExist:
            return Response({'message': '未找到该日记'}, status=status.HTTP_400_BAD_REQUEST)
        if not Approval.objects.filter(user=request.user, dairy=dairy).exists():
            approval = Approval(user=request.user, dairy=dairy)
            approval.save()
            action_type = 1
        else:
            Approval.objects.filter(user=request.user, dairy=dairy).delete()
            action_type = 0
        return Response({'message': '操作成功', 'action': action_type}, status=status.HTTP_200_OK)

    @detail_route(methods=('post',))
    def comment(self, request, pk=None, *args, **kwargs):
        content = request.data.get('content', '')
        if not content:
            return Response({'message': '请填写内容'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            dairy = Daily.objects.get(id=pk)
        except Daily.DoesNotExist:
            return Response({'message': '未找到该日记'}, status=status.HTTP_400_BAD_REQUEST)
        comment = Comment(user=request.user, dairy=dairy, content=content)
        comment.save()
        return Response({'message': '操作成功'}, status=status.HTTP_200_OK)

    @detail_route(methods=('get',))
    def approved(self, request, pk=None, *args, **kwargs):
        queryset = Approval.objects.filter(dairy_id=pk)
        # 最多取前10条
        queryset = queryset[:10]
        serializer = ApprovedUserSerializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(methods=('get',))
    def commented(self, request, pk=None, *args, **kwargs):
        queryset = Comment.objects.filter(dairy_id=pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)
