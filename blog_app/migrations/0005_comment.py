# Generated by Django 4.0 on 2022-01-02 18:13

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
        ('blog_app', '0004_alter_post_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('body', models.TextField(help_text='Put your brief comment in 500 characters', max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.UUID('7603fbe7-e509-4018-ba85-65c14a3a2213'), editable=False, primary_key=True, serialize=False, unique=True)),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.profile')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_app.post')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
