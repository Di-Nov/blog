# Generated by Django 4.2.4 on 2023-08-26 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_comments'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
        migrations.RenameIndex(
            model_name='comment',
            new_name='blog_commen_created_0e6ed4_idx',
            old_name='blog_commen_created_ad0231_idx',
        ),
    ]
