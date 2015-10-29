# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cf_s3field.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='S3FieldTestModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pic', cf_s3field.fields.S3ImageField(storage=cf_s3field.fields.S3Storage(b''), upload_to=b'')),
                ('doc', cf_s3field.fields.S3FileField(storage=cf_s3field.fields.S3Storage(b'test_file'), upload_to=b'')),
            ],
        ),
    ]
