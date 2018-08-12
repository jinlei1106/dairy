from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import list_route
from django.contrib import auth

from .models import User


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    @list_route(methods=('post',))
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = auth.authenticate(username=username, password=password)
        if not user or not user.is_authenticated():
            return Response({'message': '密码或用户名错误'}, status=status.HTTP_400_BAD_REQUEST)
        auth.login(self.request, user)
        return Response({'username': user.username}, status=status.HTTP_200_OK)

    @list_route(methods=('post',))
    def signup(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            return Response({'message': '用户名已被使用'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        return Response({'message': '用户 {0} 注册成功'.format(user.username)}, status=status.HTTP_200_OK)

    @list_route()
    def logout(self, request):
        auth.logout(request)
        return Response({'message': '登出成功'}, status=status.HTTP_200_OK)
