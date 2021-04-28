# Create your views here.
from django.shortcuts import render, redirect

# Add the following import
from django.http import HttpResponse

# Our Models
from .models import Doctor

from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# new/updated imports below
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-east-1.amazonaws.com/'
BUCKET = 'doctor-collec-inventory'


def doctor_index(request):
    doctors = Doctor.objects.all()
    context = {'doctors': doctors}
    return render(request, 'doctor/index.html', context)


def home(request):
    return render(request, 'home.html')


class DoctorUpdate(UpdateView):
    model = Doctor
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ['name', 'description', 'specialty']


class DoctorDelete(DeleteView):
    model = Doctor
    success_url = '/doctors/'


class DoctorCreate(CreateView):
    model = Doctor
    fields = ['name', 'specialty', 'description']
    success_url = '/doctors/'


def doctor_detail(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)

    context = {
        'doctor': doctor,

    }
    return render(request, 'doctor/detail.html', context)


def add_photo(request, doctor_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, doctor_id=doctor_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('index', doctor_id=doctor_id)
