import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.TextField()),
                ('last', models.TextField()),
                ('email', models.TextField()),
                ('dob', models.DateField()),
                ('image_url', models.URLField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DBRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.TextField()),
                ('title', models.TextField()),
                ('ingredients', models.TextField()),
                ('instructions', models.TextField()),
                ('url', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('account1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account1', to='recipe.account')),
                ('account2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account2', to='recipe.account')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.ImageField(blank=True, upload_to='')),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.account')),
                ('db_recipe', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='recipe.dbrecipe')),
            ],
        ),
        migrations.CreateModel(
            name='UserRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('ingredients', models.TextField()),
                ('instructions', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.account')),
            ],
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.AddField(
            model_name='likes',
            name='user_recipe',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='recipe.userrecipe'),
        ),
        migrations.AddField(
            model_name='image',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.userrecipe'),
        ),
    ]
