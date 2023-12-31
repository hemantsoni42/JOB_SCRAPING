# Generated by Django 4.1.12 on 2023-10-24 17:38

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('Title', models.CharField(max_length=200)),
                ('Company', models.CharField(max_length=200)),
                ('Experience', models.CharField(max_length=100)),
                ('Salary', models.CharField(max_length=100)),
                ('Location', models.CharField(max_length=100)),
                ('URL', models.URLField()),
                ('Skills', models.TextField()),
            ],
        ),
    ]
