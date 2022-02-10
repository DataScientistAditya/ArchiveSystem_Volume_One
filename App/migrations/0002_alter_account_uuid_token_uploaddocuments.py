# Generated by Django 4.0.2 on 2022-02-10 10:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='UUid_Token',
            field=models.UUIDField(default='1af6d45d-fb57-4f02-9ddf-474efc46c4a0', editable=False),
        ),
        migrations.CreateModel(
            name='UploadDocuments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Document', models.FileField(upload_to='documents/')),
                ('Thumbnail', models.ImageField(upload_to='images/')),
                ('Category', models.CharField(choices=[('select', 'select'), ('history', 'history'), ('literature', 'literature'), ('philosophy', 'philosophy'), ('psychology', 'psychology'), ('science', 'science')], default='Select', max_length=20)),
                ('Language', models.CharField(choices=[('select', 'select'), ('history', 'history'), ('literature', 'literature'), ('philosophy', 'philosophy'), ('psychology', 'psychology'), ('science', 'science')], default='Select', max_length=20)),
                ('DateCreated', models.DateTimeField(auto_now_add=True)),
                ('UserId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]