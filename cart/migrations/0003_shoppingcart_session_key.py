# Generated by Django 4.2 on 2023-04-25 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_alter_shoppingcart_total_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='session_key',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
