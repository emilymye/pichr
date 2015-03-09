from django.db import models


class SCTMorphology(models.Model):
    name = models.CharField(max_length=100)
    sctid = models.IntegerField(primary_key=True)
    general = models.BooleanField(default=False)

    def __str__(self):
        return self.name 


class SCTBodyStructure(models.Model):
    class Meta:
        ordering = ['name']

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
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name


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
    
    sct_injury = models.ForeignKey("SCTInjury")
    player = models.ForeignKey("Player")

    def diffERA(self):
        return self.postERA - self.preERA

    def diffFastball(self):
        return self.postFastball - self.preFastball

    def labels(self):
        label, weight = 0, 2
        if self.postERA - self.preERA < self.RANK_CUTOFFS["era"]:
            weight+=1
        if self.postFastball - self.preFastball > self.RANK_CUTOFFS["era"]:
            weight+=1

        if self.reinjury:
            label = 1
            weight -= 1.5
        if self.offseason:
            label = 2 if not self.reinjury else 3
            weight -= 0.5

        return label, weight