from django.db import models
from django.contrib.auth.models import User
class Tracker(models.Model):
    Type_choices=[('Income','Income'),
                 ('Expense','Expense'),
                 ]
    title=models.CharField(max_length=255)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    type=models.CharField(max_length=100,choices=Type_choices)
    category=models.CharField(max_length=100)
    date=models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


