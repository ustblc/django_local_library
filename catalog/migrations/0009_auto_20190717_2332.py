# Generated by Django 2.2.3 on 2019-07-17 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20190717_2326'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Set book as returned'),)},
        ),
    ]