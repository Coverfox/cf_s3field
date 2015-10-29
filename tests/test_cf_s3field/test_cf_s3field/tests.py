from django import forms
from django.test import TestCase
from django.conf import settings
from django.test import Client

import os
import re

from test_cf_s3field.models import S3FieldTestModel


class FieldTestForm(forms.ModelForm):
    class Meta:
        model = S3FieldTestModel
        fields = ["pic", "doc"]


class TestImageField(TestCase):
    def setUp(self):
        self.client = Client()

    def test_upload_files(self):
        # Upload image with form.
        cur_dir = os.path.dirname(os.path.realpath("__file__"))
        response = self.client.post(
            '/upload/',
            {
                "pic": open(os.path.join(cur_dir, "test_cf_s3field", "image.jpg")),
                "doc": open(os.path.join(cur_dir, "test_cf_s3field", "doc.txt"))
            }
        )
        self.assertEqual('SUCCESS', response.content)
        instance = S3FieldTestModel.objects.all().first()
        pic_reg = r'^test_pic\_[0-9]{1}\_[0-9]+\.jpg$'.replace("[0-9]{1}", "[%s]" % instance.pk)
        doc_reg = r'^test_file\_[0-9]{1}\_[0-9]+\.txt$'.replace("[0-9]{1}", "[%s]" % instance.pk)
        self.assertEqual(
            True,
            bool(re.search(pic_reg, instance.pic.name))
        )
        self.assertEqual(
            True,
            bool(re.search(doc_reg, instance.doc.name))
        )
        pic = instance.pic.name
        doc = instance.doc.name

        response = self.client.post(
            '/upload/?id=%s' % S3FieldTestModel.objects.all().first().pk,
            {
                "pic": open(os.path.join(cur_dir, "test_cf_s3field", "image2.jpg")),
                "doc": open(os.path.join(cur_dir, "test_cf_s3field", "doc2.txt"))
            }
        )

        # File update test
        self.assertEqual('SUCCESS', response.content)
        self.assertEqual(
            True,
            bool(re.search(pic_reg, instance.pic.name))
        )
        self.assertEqual(
            True,
            bool(re.search(doc_reg, instance.doc.name))
        )

        # Old file delete test
        self.assertEqual(hasattr(settings, pic), True)
        self.assertEqual(hasattr(settings, doc), True)
