# Generated by Django 4.2.2 on 2023-06-16 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(help_text='Error message', max_length=255)),
                ('stack_trace', models.TextField(help_text='Stack Trace')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Time at which the error occurred')),
            ],
        ),
    ]
