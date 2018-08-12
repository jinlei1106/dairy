from rest_framework import serializers

from .models import Daily


class DairyListSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Daily
        fields = ('id', 'title', 'content', 'created', 'updated', 'username')

    def get_username(self, obj):
        return obj.user.username

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(DairyListSerializer, self).create(validated_data)


class ApprovedUserSerializer(serializers.Serializer):
    username = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', source='created')

    class Meta:
        fields = ('username', 'create_time')

    def get_username(self, obj):
        return obj.user.username


class CommentSerializer(serializers.Serializer):
    username = serializers.SerializerMethodField()
    content = serializers.CharField()
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', source='created')

    class Meta:
        fields = ('username', 'content', 'create_time')

    def get_username(self, obj):
        return obj.user.username
