from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=50,unique=True)
    create_date = models.DateField(default=timezone.now)
    members = models.ManyToManyField(User,through='Membership')
    max_users = models.PositiveSmallIntegerField(default=10,validators=[MaxValueValidator(50)])
    starting_value = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal("10000.00"))
    @property
    def numUsers(self):
        return self.members.count()

    def __str__(self):
        return self.name

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    creator = models.BooleanField(default=False)
    date_join = models.DateField(default=timezone.now)
    total_asset_value = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal("10000.00"))
    cash_remaining = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal("10000.00"))
    stock_value = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal("0.00"))
    rank = models.PositiveSmallIntegerField(default=None,blank=True,null=True,validators=[MaxValueValidator(50)])

    def __str__(self):
        return str(self.user) + "__" + str(self.room)

class Transaction(models.Model):
    member = models.ForeignKey(Membership,on_delete=models.CASCADE,null=True)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)],null=True)
    price = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal("0.0"))
    date = models.DateTimeField(default=timezone.now, editable=False)
    ticker = models.CharField(max_length=20,null=True,default="")

    def __str__(self):
        return str(self.member.user.username) + "__" + str(self.member.room.name) + str(self.id)


class Saved_Stock(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ticker = models.CharField(max_length=20,null=True,default="")
    date_added = models.DateTimeField(default=timezone.now,editable=False)
    initial_price = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal("0.0"))

    def __str__(self):
        return str(self.user) + "__" + str(self.ticker)