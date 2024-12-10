from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0008_cookbook_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='cookbook',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
