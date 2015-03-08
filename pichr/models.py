from django.db import models


class InjuryType(models.Model):
    name = models.CharField(max_length=100)
    sctid = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.name 

class InjuryLocation(models.Model):
    name = models.CharField(max_length=100)
    sctname = models.CharField(max_length=200)
    sctid = models.IntegerField(primary_key=True)
    children = models.ManyToManyField("InjuryLocation", related_name="parents")
    descendants = models.ManyToManyField("InjuryLocation", related_name="ancestors")

    root = models.BooleanField(default=False)

    def __str__(self):
        return self.name 

class Procedure(models.Model):
    name = models.CharField(max_length=100)
    sctid = models.IntegerField(primary_key=True)

    procedure_site = models.ForeignKey("InjuryLocation", null=True)
    def __str__(self):
        return self.name 

class RecoveryStatistic(models.Model):
    date = models.DateField()
    duration = models.IntegerField()

    preERA = models.FloatField()
    postERA = models.FloatField()
    preFastball = models.FloatField()
    postFastball = models.FloatField()

    reinjury = models.BooleanField(default=False)
    offseason = models.BooleanField(default=False)
    procedure = models.ForeignKey("Procedure", null=True)
    
    def weight(self):
        return 1.0


class Player(models.Model):
    name = models.CharField(max_length=200)
    pid = models.IntegerField(primary_key=True)
    team = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name 

class Injury(models.Model):
    name = models.CharField(max_length=200)
    sctid = models.IntegerField(default=-1)

    injury_type = models.ForeignKey("InjuryType")
    injury_location = models.ForeignKey("InjuryLocation")

    player = models.ForeignKey("Player")
    recovery = models.OneToOneField("RecoveryStatistic")

    def __str__(self):
        return self.name 

