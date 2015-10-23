from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from files import FileField, ImageField
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files import File

from boto.s3.connection import S3Connection
from boto.s3.key import Key

import django
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


class S3Storage(FileSystemStorage):

    def __init__(self, bucket=None, location=None, base_url=None):
        assert bucket
        location = settings.MEDIA_ROOT

        if base_url is None:
            base_url = settings.MEDIA_URL
        self.location = os.path.abspath(location)
        self.bucket = bucket
        self.base_url = base_url

    def _open(self, name, mode='rb'):
        return S3File(Key(self.bucket, name))

    def _save(self, name, content):
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
        self.bucket.delete_key(name.split("/")[-1])

    def exists(self, name):
        return Key(self.bucket, name).exists()

    def listdir(self, path):
        return [key.name for key in self.bucket.list()]

    def path(self, name):
        raise NotImplementedError

    def size(self, name):
        return self.bucket.get_key(name).size

    def url(self, name):
        cname = name.split("/", 3)[3]
        return Key(self.bucket, cname).generate_url(100000)

    def get_available_name(self, name):
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
        migrate = kwargs.get("migrate", True)
        
        if not migrate:
            self.connection = S3Connection(
                settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY
            )
            if not self.connection.lookup(bucket):
                self.connection.create_bucket(bucket)
            self.bucket = self.connection.get_bucket(bucket)
            storage = S3Storage(self.bucket)
        
        if kwargs.has_key("migrate"):
            del kwargs["migrate"]
            
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
        import pdb; pdb.set_trace()
        migrate = kwargs.get("migrate", True)
            
        if not migrate:
            self.connection = S3Connection(
                settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY
            )
            # If bucket does not exist then create new.
            if not self.connection.lookup(bucket):
                self.connection.create_bucket(bucket)
            self.bucket = self.connection.get_bucket(bucket)
            kwargs['storage'] = S3Storage(self.bucket)
        
        if kwargs.has_key("migrate"):
            del kwargs["migrate"]
        
        super(S3ImageField, self).__init__(
            verbose_name, name, width_field, height_field, key=key, **kwargs
        )

