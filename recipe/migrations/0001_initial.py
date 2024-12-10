from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.TextField()),
                ('last', models.TextField()),
                ('city', models.TextField()),
                ('email', models.TextField()),
                ('image_url', models.URLField(blank=True)),
            ],
        ),
    ]
