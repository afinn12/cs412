from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0007_cookbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='cookbook',
            name='name',
            field=models.TextField(default='Favorites'),
            preserve_default=False,
        ),
    ]
