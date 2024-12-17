# Generated by Django 5.1.4 on 2024-12-17 14:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Author', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('b_id', models.AutoField(primary_key=True, serialize=False)),
                ('b_title', models.CharField(blank=True, max_length=255, null=True)),
                ('isbn', models.CharField(blank=True, max_length=13, null=True, unique=True)),
                ('available_copies', models.IntegerField(blank=True, null=True)),
                ('author', models.ForeignKey(blank=True, db_column='author', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Author.author')),
            ],
            options={
                'db_table': 'book',
            },
        ),
        migrations.CreateModel(
            name='Borrowrecord',
            fields=[
                ('r_id', models.AutoField(primary_key=True, serialize=False)),
                ('borrowed_by', models.CharField(blank=True, max_length=255, null=True)),
                ('borrow_date', models.DateField(blank=True, null=True)),
                ('return_date', models.DateField(blank=True, null=True)),
                ('book', models.ForeignKey(blank=True, db_column='Book', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Book.book')),
            ],
            options={
                'db_table': 'borrowrecord',
            },
        ),
    ]
