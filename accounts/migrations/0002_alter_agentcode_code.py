# Generated by Django 5.1.3 on 2024-11-14 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentcode',
            name='code',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
