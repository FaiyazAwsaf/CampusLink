# Generated by Django 5.2.3 on 2025-07-19 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entrepreneurs_hub', '0005_alter_storefront_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storefront',
            name='image',
            field=models.URLField(blank=True, default='https://images.pexels.com/photos/789327/pexels-photo-789327.jpeg', null=True),
        ),
    ]
