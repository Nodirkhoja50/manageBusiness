# Generated by Django 4.2.2 on 2023-07-06 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_pastel_xisob_alter_rulon_information_pastel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rulon',
            name='information_pastel',
            field=models.FileField(upload_to='D:\\REPO\\PastelBot\\'),
        ),
    ]
