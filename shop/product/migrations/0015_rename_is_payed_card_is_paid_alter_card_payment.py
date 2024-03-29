# Generated by Django 5.0.1 on 2024-01-31 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_remove_factoritems_factory_profit_factor_card'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='is_payed',
            new_name='is_paid',
        ),
        migrations.AlterField(
            model_name='card',
            name='payment',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
