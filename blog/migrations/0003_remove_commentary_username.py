# Generated by Django 3.0.3 on 2020-04-09 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200328_0047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentary',
            name='username',
        ),
    ]
