# Generated by Django 2.1.1 on 2018-09-12 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='date',
            field=models.CharField(help_text='YYYYMMDD', max_length=15),
        ),
    ]
