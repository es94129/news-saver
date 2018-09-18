# Generated by Django 2.1.1 on 2018-09-13 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20180914_0029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spell', models.CharField(blank=True, max_length=20, null=True)),
                ('newss', models.ManyToManyField(help_text='The news that use this word.', to='blog.News')),
            ],
        ),
    ]