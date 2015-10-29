from django.db import models

from cf_s3field.fields import S3ImageField, S3FileField


class S3FieldTestModel(models.Model):
    pic = S3ImageField(bucket='test_pic', key="test_pic_{uid}_")
    doc = S3FileField(bucket='test_file', key="test_file_{uid}_")
