from django.db import models

# Create your models here.


class Predictions(models.Model):
    created=models.DateTimeField(auto_now_add=True)
    sym_name=models.CharField(max_length=10)
    sym_prediction=models.FloatField()

    def __str__(self):
        return self.sym_name


