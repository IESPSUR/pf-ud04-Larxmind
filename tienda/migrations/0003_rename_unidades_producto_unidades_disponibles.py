# Generated by Django 4.1.3 on 2022-11-20 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0002_rename_unidades_compra_unidades_solicitadas'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='unidades',
            new_name='unidades_disponibles',
        ),
    ]
