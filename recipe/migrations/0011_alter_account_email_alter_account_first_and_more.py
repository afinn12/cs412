from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0010_alter_cookbook_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='account',
            name='first',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='account',
            name='last',
            field=models.CharField(max_length=64),
        ),
    ]
