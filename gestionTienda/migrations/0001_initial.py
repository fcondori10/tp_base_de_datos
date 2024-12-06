# Generated by Django 5.1.3 on 2024-12-05 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('dni', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('telefono', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Pedidos',
            fields=[
                ('id_pedido', models.AutoField(primary_key=True, serialize=False)),
                ('id_producto', models.IntegerField()),
                ('dni', models.IntegerField()),
                ('cantidad', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('id_producto', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('categoria', models.CharField(max_length=50)),
            ],
        ),
    ]
