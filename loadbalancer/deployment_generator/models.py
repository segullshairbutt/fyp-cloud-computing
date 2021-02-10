from django.db import models


class Node(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(default=2)


class Image(models.Model):
    PENDING = "Pending"
    PUSHED = "Pushed"
    VANISH_ABLE = "VANISH_ABLE"

    project_id = models.IntegerField()
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=50, default=PENDING)
