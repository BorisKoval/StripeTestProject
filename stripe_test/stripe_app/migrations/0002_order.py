# Generated by Django 4.1.6 on 2023-02-11 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_cost', models.FloatField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('items', models.ManyToManyField(to='stripe_app.item')),
            ],
        ),
    ]
