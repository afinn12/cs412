import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0003_rename_likes_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='db_recipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='recipe.dbrecipe'),
        ),
        migrations.AlterField(
            model_name='like',
            name='user_recipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='recipe.userrecipe'),
        ),
    ]
