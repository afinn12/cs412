# Generated by Django 5.1.2 on 2024-11-12 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter_analytics', '0003_alter_voter_apartment_alter_voter_dob_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='dob',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='dor',
            field=models.DateField(),
        ),
    ]