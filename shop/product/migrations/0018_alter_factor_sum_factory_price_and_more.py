# Generated by Django 5.0.1 on 2024-02-03 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_remove_item_card_remove_factor_card_item_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factor',
            name='sum_factory_price',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='factor',
            name='sum_total_price',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='factor',
            name='sum_total_profit',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='factor',
            name='sum_unit_price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]