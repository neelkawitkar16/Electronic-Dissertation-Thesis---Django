# Generated by Django 3.1.2 on 2021-04-08 02:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_claimmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='claimmodel',
            name='claim_num',
        ),
    ]
