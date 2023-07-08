# Generated by Django 4.2.2 on 2023-06-30 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pastel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('big_pastel', models.IntegerField(default=10)),
                ('small_pastel', models.IntegerField(default=0)),
                ('nalichka', models.IntegerField(default=0)),
                ('gastiniy', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'pastel',
                'verbose_name_plural': 'pastel',
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_big', models.CharField(max_length=50)),
                ('price_small', models.CharField(max_length=50)),
                ('price_nalichka', models.CharField(max_length=50)),
                ('price_gastiniy', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Rulon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rulon', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]