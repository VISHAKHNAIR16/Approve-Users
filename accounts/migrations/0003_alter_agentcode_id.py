# Generated by Django 5.1.3 on 2024-11-14 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_agentcode_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentcode',
            name='id',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
