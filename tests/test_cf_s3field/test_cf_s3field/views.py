from django.http import HttpResponse

from test_cf_s3field.tests import FieldTestForm
from test_cf_s3field.models import S3FieldTestModel


def upload_file(request):
    if request.method == 'POST':
        instance = None
        if request.GET.get("id"):
            instance = S3FieldTestModel.objects.get(id=request.GET["id"])

        form = FieldTestForm(request.POST, request.FILES, instance=instance)
        if not form.is_valid():
            return HttpResponse("NOFILE")

        form.instance.uid = 1
        form.save()
        return HttpResponse("SUCCESS")
