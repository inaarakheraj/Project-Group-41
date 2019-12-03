from django.db import models


class Sighting(models.Model):
    Latitude = models.FloatField()
    Longitude = models.FloatField()
    Unique_Squirrel_ID = models.CharField(primary_key=True, max_length=20)
    Shift = models.CharField(max_length=2)
    Date = models.CharField(max_length=8)
    Age = models.CharField(max_length=10,null=True,blank=True)
    Primary_Fur_Color = models.CharField(max_length=10,null=True,blank=True)
    Location = models.CharField(max_length=20,null=True,blank=True)
    Specific_Location = models.CharField(max_length=30,null=True,blank=True)
    Running = models.BooleanField()
    Chasing = models.BooleanField()
    Climbing = models.BooleanField()
    Eating = models.BooleanField()
    Foraging = models.BooleanField()
    Other_Activities = models.CharField(max_length=20,null=True,blank=True)
    Kuks = models.BooleanField()
    Quaas = models.BooleanField()
    Moans = models.BooleanField()
    Tail_flags = models.BooleanField()
    Tail_twitches = models.BooleanField()
    Approaches = models.BooleanField()
    Indifferent = models.BooleanField()
    Runs_from = models.BooleanField()

    def __str__(self):
        return self.Unique_Squirrel_ID