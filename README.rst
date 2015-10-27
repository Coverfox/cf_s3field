Django has ImageField and FileField which can be used for file and image operations. Django fields has problem that they store image and files on disk. They also don't delete older files when new files are uploaded. To solve this issue new field developed.  

cf_s3field.S3ImageField
-----------------------
``s3ImageField`` is django model field which is replacement for django ``ImageField``. 
```python
from cf_s3field.files import S3ImageField

class User(models.Model):
    first_name = models.CharField(max_length=100)
    profile_pic = S3ImageField(bucket='<your bucket>', key='profile_user_{first_name}')
    
user = User.objects.get(id=1)
user.first_name = "Hitul"
user.save()
```
In above example key ``first_name`` will be replaced by ``Hitul``. ImageField will also accept default django ImageField parameters. key is file name format. In s3 you will store multiple files. To seperate all images from each other key is introduced. Key values will be repalced by values specified in as extra attributes.

cf_s3field.S3FileField
-----------------------
``s3FileField`` is django model field which is replacement for django ``FileField``. 
```python
from cf_s3field.files import S3ImageField

class User(models.Model):
    first_name = models.CharField(max_length=100)
    resume = S3FileField(bucket='<your bucket>', key='profile_user_{first_name}')
    
user = User.objects.get(id=1)
user.first_name = "Hitul"
user.save()
```
