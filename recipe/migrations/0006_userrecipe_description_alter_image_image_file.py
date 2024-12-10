from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_dbrecipe_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrecipe',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='image_file',
            field=models.ImageField(upload_to=''),
        ),
    ]
