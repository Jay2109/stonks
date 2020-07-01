from django.db import models

# Create your models here.


class Sentimentor(models.Model):
    created=models.DateTimeField(auto_now_add=True)
    general_sentiment=models.CharField(max_length=15)

    def __str__(self):
        return self.general_sentiment

class Tickersentiment(models.Model):
    created=models.DateTimeField(auto_now_add=True)
    sym_name=models.CharField(max_length=12)
    sentiment=models.CharField(max_length=15)

    def __str__(self):
        return self.sym_name
    


