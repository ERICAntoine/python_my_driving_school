# Generated by Django 3.0.5 on 2020-04-12 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200412_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Role'),
        ),
    ]
