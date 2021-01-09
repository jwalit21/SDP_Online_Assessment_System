# Generated by Django 3.1.5 on 2021-01-09 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lab', '0001_initial'),
        ('contest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('problemId', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='DEFAULT-TITLE', max_length=50)),
                ('description', models.CharField(default='Default Problem description', max_length=1000)),
                ('difficulty', models.CharField(choices=[('EASY', 'EASY'), ('MEDIUM', 'MEDIUM'), ('HARD', 'HARD')], max_length=6)),
                ('points', models.IntegerField()),
                ('durationTime', models.IntegerField()),
                ('doesBelongToContest', models.BooleanField(default=False)),
                ('contestId', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='contest.contest')),
                ('labId', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='lab.lab')),
            ],
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('testCaseId', models.AutoField(primary_key=True, serialize=False)),
                ('inputFile', models.FileField(max_length=254, upload_to=None)),
                ('outputFile', models.FileField(max_length=254, upload_to=None)),
                ('problemId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.problem')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemComment',
            fields=[
                ('pcId', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.CharField(max_length=2000)),
                ('problemId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.problem')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
