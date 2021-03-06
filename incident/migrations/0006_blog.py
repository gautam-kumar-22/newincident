# Generated by Django 2.2.7 on 2019-12-15 10:49

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('incident', '0005_auto_20191215_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='title')),
                ('discription', ckeditor_uploader.fields.RichTextUploadingField()),
                ('is_enable', models.NullBooleanField(default=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_user', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
    ]
