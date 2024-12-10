from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0009_cookbook_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cookbook',
            name='name',
            field=models.CharField(max_length=64),
        ),
    ]
