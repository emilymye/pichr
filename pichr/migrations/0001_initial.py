# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('pid', models.IntegerField(serialize=False, primary_key=True)),
                ('team', models.CharField(default=b'', max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recovery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('duration', models.IntegerField()),
                ('preERA', models.FloatField()),
                ('postERA', models.FloatField()),
                ('preFastball', models.FloatField()),
                ('postFastball', models.FloatField()),
                ('reinjury', models.BooleanField(default=False)),
                ('offseason', models.BooleanField(default=False)),
                ('player', models.ForeignKey(to='pichr.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SCTBodyStructure',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('sctname', models.CharField(max_length=200)),
                ('sctid', models.IntegerField(serialize=False, primary_key=True)),
                ('root', models.BooleanField(default=False)),
                ('children', models.ManyToManyField(related_name='parents', to='pichr.SCTBodyStructure')),
                ('descendants', models.ManyToManyField(related_name='ancestors', to='pichr.SCTBodyStructure')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SCTInjury',
            fields=[
                ('sctid', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('finding_site', models.ForeignKey(to='pichr.SCTBodyStructure')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SCTMorphology',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('sctid', models.IntegerField(serialize=False, primary_key=True)),
                ('general', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SCTProcedure',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('sctid', models.IntegerField(serialize=False, primary_key=True)),
                ('procedure_site', models.ForeignKey(to='pichr.SCTBodyStructure', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sctinjury',
            name='morphology',
            field=models.ForeignKey(to='pichr.SCTMorphology'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='recovery',
            name='procedure',
            field=models.ForeignKey(to='pichr.SCTProcedure', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='recovery',
            name='sct_injury',
            field=models.ForeignKey(to='pichr.SCTInjury'),
            preserve_default=True,
        ),
    ]
