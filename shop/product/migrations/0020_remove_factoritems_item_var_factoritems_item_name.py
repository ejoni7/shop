# Generated by Django 5.0.1 on 2024-02-03 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0019_factor_transfer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factoritems',
            name='item_var',
        ),
        migrations.AddField(
            model_name='factoritems',
            name='item_name',
            field=models.CharField(default='fvfdfsfdfffffffffffffffffff', max_length=150),
            preserve_default=False,
        ),
    ]
