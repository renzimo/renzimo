# Generated by Django 3.1.7 on 2021-03-13 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projects',
            options={'ordering': ['id'], 'verbose_name': '项目信息', 'verbose_name_plural': '项目信息'},
        ),
    ]
