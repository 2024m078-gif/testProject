from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 100)
    def _str_(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField()
    price = models.IntegerField()
    category = models.ForeignKey(
        "Category",
        on_delete = models.CASCADE
    )
    def _str (self):
        return self.name
