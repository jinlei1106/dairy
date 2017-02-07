from rest_framework import serializers

from .models import Daily


class DariyListSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    approvals = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Daily
        fields = ('id', 'title', 'content', 'created', 'updated', 'username', 'approvals', 'comments')

    def get_username(self, obj):
        return obj.user.username

    def get_approvals(self, obj):
        a_users = []
        approvals = obj.approvals.all()
        for approval in approvals:
            a_users.append(approval.user.username)
        return a_users

    def get_comments(self, obj):
        c_users = []
        comments = obj.comments.all()
        for comment in comments:
            c_users.append({
                'user': comment.user.username,
                'content': comment.content
            })
        return c_users

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(DariyListSerializer, self).create(validated_data)