# Generated by Django 3.2.8 on 2021-10-29 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_miscard'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('miscard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='shop.miscard')),
            ],
        ),
    ]