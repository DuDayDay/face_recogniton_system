# Generated by Django 4.1 on 2024-04-13 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentinfo',
            name='ImgUrl',
            field=models.URLField(default='http:', verbose_name='图像地址'),
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='StudentID',
            field=models.CharField(default='xxx', max_length=10, verbose_name='学号'),
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='age',
            field=models.IntegerField(default=0, verbose_name='年龄'),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='name',
            field=models.CharField(default='zhan', max_length=10, verbose_name='姓名'),
        ),
    ]
