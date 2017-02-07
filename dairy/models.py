from django.db import models

from apps.user.models import User


class Daily(models.Model):
    user = models.ForeignKey(User, related_name='dairies')
    title = models.CharField(max_length=30)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    share = models.BooleanField(default=True)

    class Meta:
        db_table = 'dairy'
        ordering = ('-updated', 'title')
