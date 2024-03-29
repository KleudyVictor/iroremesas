# Generated by Django 4.2.7 on 2024-02-18 03:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mensajero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('ci', models.CharField(max_length=11, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='transaccion',
            name='mensajero',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mensajero', to='polls.mensajero'),
        ),
    ]
