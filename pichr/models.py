from django.db import models


class SCTMorphology(models.Model):
    name = models.CharField(max_length=100)
    sctid = models.IntegerField(primary_key=True)
    general = models.BooleanField(default=False)

    def __str__(self):
        return self.name 


class SCTBodyStructure(models.Model):
    name = models.CharField(max_length=100)
    sctname = models.CharField(max_length=200)
    sctid = models.IntegerField(primary_key=True)
    children = models.ManyToManyField("SCTBodyStructure", related_name="parents")
    descendants = models.ManyToManyField("SCTBodyStructure", related_name="ancestors")

    root = models.BooleanField(default=False)

    def __str__(self):
        return self.name 


class SCTInjury(models.Model):
    sctid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    finding_site = models.ForeignKey("SCTBodyStructure")
    morphology = models.ForeignKey("SCTMorphology")


class SCTProcedure(models.Model):
    name = models.CharField(max_length=100)
    sctid = models.IntegerField(primary_key=True)

    procedure_site = models.ForeignKey("SCTBodyStructure", null=True)
    def __str__(self):
        return self.name 


class Player(models.Model):
    name = models.CharField(max_length=200)
    pid = models.IntegerField(primary_key=True)
    team = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name 


class Recovery(models.Model):
    RANK_CUTOFFS = {
        "era": 0.25,
        "fastball": 0.2
    }

    date = models.DateField()
    duration = models.IntegerField()

    preERA = models.FloatField()
    postERA = models.FloatField()
    preFastball = models.FloatField()
    postFastball = models.FloatField()

    reinjury = models.BooleanField(default=False)
    offseason = models.BooleanField(default=False)
    procedure = models.ForeignKey("SCTProcedure", null=True)
    
    def rank(self):
        rank = 1
        if self.postERA - self.preERA < self.RANK_CUTOFFS["era"]:
            rank+=1
        if self.postFastball - self.preFastball > self.RANK_CUTOFFS["era"]:
            rank+=1
        if self.reinjury:
            rank -= 2
        if offseason:
            rank -= 1

        return min(rank, 0)


class Injury(models.Model):
    sct_injury = models.ForeignKey("SCTInjury")
    player = models.ForeignKey("Player")
    recovery = models.OneToOneField("Recovery")

    def __str__(self):
        return "%s for %s" % (self.sct_injury.name, self.player.name) 

