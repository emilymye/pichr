# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Injury',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('sctid', models.IntegerField(default=-1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InjuryLocation',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('sctname', models.CharField(max_length=200)),
                ('sctid', models.IntegerField(serialize=False, primary_key=True)),
                ('root', models.BooleanField(default=False)),
                ('children', models.ManyToManyField(related_name='parents', to='pichr.InjuryLocation')),
                ('descendants', models.ManyToManyField(related_name='ancestors', to='pichr.InjuryLocation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InjuryType',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('sctid', models.IntegerField(serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
            name='Procedure',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('sctid', models.IntegerField(serialize=False, primary_key=True)),
                ('procedure_site', models.ForeignKey(to='pichr.InjuryLocation', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RecoveryStatistic',
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
                ('procedure', models.ForeignKey(to='pichr.Procedure', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='injury',
            name='injury_location',
            field=models.ForeignKey(to='pichr.InjuryLocation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='injury',
            name='injury_type',
            field=models.ForeignKey(to='pichr.InjuryType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='injury',
            name='player',
            field=models.ForeignKey(to='pichr.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='injury',
            name='recovery',
            field=models.OneToOneField(to='pichr.RecoveryStatistic'),
            preserve_default=True,
        ),
    ]
