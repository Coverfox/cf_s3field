from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from files import FileField, ImageField
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files import File

from boto.s3.connection import S3Connection
from boto.s3.key import Key

import os


class S3File(File):
    def __init__(self, key):
        self.key = key

    def size(self):
        return self.key.size

    def read(self, *args, **kwargs):
        return self.key.read(*args, **kwargs)

    def write(self, content):
        self.key.set_contents_from_string(content)

    def close(self):
        self.key.close()

if getattr(settings, "TESTING"):
    class S3Storage(FileSystemStorage):

        def __init__(self, bucket=None, location=None, base_url=None):
            self.bucket = bucket
            self.connected = False

        def _do_connection(self):
            assert self.bucket
            self.connected = True

        def _open(self, name, mode='rb'):
            if not self.connected:
                self._do_connection()

            return name

        def _save(self, name, content):
            if not self.connected:
                self._do_connection()
            return content.name

        def delete(self, name):
            if not self.connected:
                self._do_connection()
            setattr(settings, name, True)

        def exists(self, name):
            if not self.connected:
                self._do_connection()

            return True

        def listdir(self, path):
            if not self.connected:
                self._do_connection()

            return []

        def path(self, name):
            if not self.connected:
                self._do_connection()

            raise NotImplementedError

        def size(self, name):
            if not self.connected:
                self._do_connection()

            return 123

        def url(self, name):
            if not self.connected:
                self._do_connection()

            return "https://s3.amazon.com/url"

        def get_available_name(self, name):
            if not self.connected:
                self._do_connection()

            return name
else:
    class S3Storage(FileSystemStorage):

        def __init__(self, bucket=None, location=None, base_url=None):
            location = settings.MEDIA_ROOT

            if base_url is None:
                base_url = settings.MEDIA_URL
            self.location = os.path.abspath(location)
            self.bucket = bucket
            self.base_url = base_url
            self.connected = False

        def _do_connection(self):
            assert self.bucket
            self.connection = S3Connection(
                settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY
            )

            if not self.connection.lookup(self.bucket):
                self.connection.create_bucket(self.bucket)

            self.bucket = self.connection.get_bucket(self.bucket)
            self.connected = True

        def _open(self, name, mode='rb'):
            if not self.connected:
                self._do_connection()

            return S3File(Key(self.bucket, name))

        def _save(self, name, content):
            if not self.connected:
                self._do_connection()

            name = content.name
            key = Key(self.bucket, name)
            if hasattr(content, 'temporary_file_path'):
                key.set_contents_from_filename(content.temporary_file_path())
            elif isinstance(content, File):
                key.set_contents_from_file(content)
            else:
                key.set_contents_from_string(content)

            return "https://%s.s3.amazonaws.com/%s" % (self.bucket.name, name)

        def delete(self, name):
            if not self.connected:
                self._do_connection()

            self.bucket.delete_key(name.split("/")[-1])

        def exists(self, name):
            if not self.connected:
                self._do_connection()

            return Key(self.bucket, name).exists()

        def listdir(self, path):
            if not self.connected:
                self._do_connection()

            return [key.name for key in self.bucket.list()]

        def path(self, name):
            if not self.connected:
                self._do_connection()

            raise NotImplementedError

        def size(self, name):
            if not self.connected:
                self._do_connection()

            return self.bucket.get_key(name).size

        def url(self, name):
            if not self.connected:
                self._do_connection()

            cname = name.split("/", 3)[3]
            return Key(self.bucket, cname).generate_url(100000)

        def get_available_name(self, name):
            if not self.connected:
                self._do_connection()

            return name


class S3FileField(FileField):

    def __init__(
        self,
        bucket='',
        verbose_name=None,
        name=None,
        upload_to='',
        storage=None,
        key=None,
        **kwargs
    ):
        if not storage:
            storage = S3Storage(bucket)

        super(S3FileField, self).__init__(
            verbose_name, name, upload_to, storage, key=key, **kwargs
        )


class S3ImageField(ImageField):
    """
        S3ImageField is django image field which will upload images to
        s3 instead of puting it on local storage.
    """
    def __init__(
        self,
        bucket='',
        verbose_name=None,
        name=None,
        width_field=None,
        height_field=None,
        key=None,
        **kwargs
    ):
        kwargs['storage'] = S3Storage(bucket)
        super(S3ImageField, self).__init__(
            verbose_name, name, width_field, height_field, key=key, **kwargs
        )

