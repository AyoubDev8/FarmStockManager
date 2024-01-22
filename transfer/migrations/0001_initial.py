# Generated by Django 3.1.13 on 2024-01-22 03:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0002_auto_20240122_0304'),
        ('centers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialTransfer',
            fields=[
                ('transfer_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity_transferred', models.PositiveIntegerField()),
                ('date_of_transfer', models.DateField()),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='centers.center')),
                ('raw_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.rawmaterial')),
            ],
        ),
    ]