from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Link(models.Model):

    url = models.CharField(unique=False,
                           max_length=256,
                           blank=False,
                           null=False)
    short_code = models.CharField(unique=True,
                                  max_length=256,
                                  blank=False,
                                  null=False)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               null=False,
                               blank=False,
                               related_name='link')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.short_code} ({self.author.username}) -> {self.url}'


class LinkStatistic(models.Model):

    link = models.ForeignKey(Link,
                             on_delete=models.CASCADE,
                             null=False,
                             blank=False,
                             related_name='linkstatistic')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=False,
                             blank=False,
                             related_name='linkstatistic')
    created_at = models.DateTimeField(auto_now_add=True)
