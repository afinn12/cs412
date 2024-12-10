import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0006_userrecipe_description_alter_image_image_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cookbook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.account')),
                ('db_recipes', models.ManyToManyField(blank=True, to='recipe.dbrecipe')),
                ('user_recipes', models.ManyToManyField(blank=True, to='recipe.userrecipe')),
            ],
        ),
    ]
