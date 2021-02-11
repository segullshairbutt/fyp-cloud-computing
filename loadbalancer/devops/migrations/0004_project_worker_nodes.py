# Generated by Django 3.0.3 on 2021-02-11 08:08

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('devops', '0003_project_initial_config'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='worker_nodes',
            field=jsonfield.fields.JSONField(default=['node1', 'node2']),
            preserve_default=False,
        ),
    ]
