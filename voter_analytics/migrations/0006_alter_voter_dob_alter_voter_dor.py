# Generated by Django 5.1.2 on 2024-11-12 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter_analytics', '0005_alter_voter_apartment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='dob',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='dor',
            field=models.TextField(),
        ),
    ]
