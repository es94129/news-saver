# Generated by Django 2.1.1 on 2018-09-13 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_news_intro'),
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ('content',),
            },
        ),
        migrations.AddField(
            model_name='news',
            name='filepath',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='word',
            name='newss',
            field=models.ManyToManyField(to='blog.News'),
        ),
    ]
