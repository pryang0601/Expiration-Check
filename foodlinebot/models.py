from django.db import models

# Create your models here.
class Food_Info(models.Model):
    name = models.CharField(max_length=255, null=False)       #食物名字
    start = models.DateField()                   #食物開始存放的日期時間
    expiration = models.DateField()              #食物過期的日期時間

    def __str__(self):
        return self.name