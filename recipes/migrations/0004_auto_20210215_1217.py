# Generated by Django 3.0.8 on 2021-02-15 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20210215_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(choices=[('breakfast', 'Завтрак'), ('lunch', 'Обед'), ('dinner', 'Ужин')], db_index=True, max_length=50, verbose_name='Имя тега'),
        ),
    ]
