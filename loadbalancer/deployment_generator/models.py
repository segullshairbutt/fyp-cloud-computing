from django.db import models


class Node(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(default=2)
