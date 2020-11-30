from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=50)
    parent_category = models.ForeignKey('self', null=True, related_name="child_types", on_delete=models.CASCADE)


class ExtraField(models.Model):
    FIELD_TYPES = [(1, "number"), (2, "text"), (3, "datetime"), (4, "year")]
    TEXT = 2

    required = models.BooleanField(default=True)
    name = models.CharField(max_length=30)
    field_type = models.SmallIntegerField(choices=FIELD_TYPES, default=TEXT)

    type = models.ForeignKey(Type, on_delete=models.CASCADE)


class Item(models.Model):
    STATES = [(1, "New"), (2, "Used")]
    NEW = 1

    title = models.CharField(max_length=80)
    code = models.CharField(max_length=30)
    description = models.CharField(max_length=250)
    model = models.CharField(max_length=30)
    aws_picture_url = models.CharField(max_length=100)

    sell_price = models.IntegerField()
    sold_price = models.IntegerField(default=0)
    state = models.SmallIntegerField(choices=STATES, default=NEW)
    is_featured = models.BooleanField(default=False)

    type = models.ForeignKey(Type, on_delete=models.SET_NULL, related_name="items")


class Auction(models.Model):
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="auctions")
