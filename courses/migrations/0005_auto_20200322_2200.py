# Generated by Django 3.0.3 on 2020-03-22 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20200227_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(blank=True, to='courses.Student'),
        ),
        migrations.AlterField(
            model_name='course',
            name='teachers',
            field=models.ManyToManyField(blank=True, to='courses.Teacher'),
        ),
    ]
