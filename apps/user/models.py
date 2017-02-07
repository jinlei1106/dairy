from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager


class DairyUserManager(UserManager):
    """
    # 自己重写manager的create_user方法，因为User表结构的原因
    """

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    objects = DairyUserManager()

    class Meta:
        db_table = 'user'
