# Generated by Django 5.1.2 on 2025-01-06 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_tag_image_alter_featured_author_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='popularity_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Популярность тега'),
        ),
    ]
