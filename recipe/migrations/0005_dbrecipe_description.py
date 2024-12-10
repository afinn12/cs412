from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_alter_like_db_recipe_alter_like_user_recipe'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbrecipe',
            name='description',
            field=models.TextField(default='Click to read more!'),
            preserve_default=False,
        ),
    ]
