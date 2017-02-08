from django.db import models

from apps.user.models import User
from dairy.models import Daily


class Approval(models.Model):
    user = models.ForeignKey(User, related_name='approved')
    dairy = models.ForeignKey(Daily, related_name='approvals')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'approval'
        ordering = ('-created',)


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='commented')
    dairy = models.ForeignKey(Daily, related_name='comments')
    content = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comment'
        ordering = ('-created',)
