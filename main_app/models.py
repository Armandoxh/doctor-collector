from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
CERTIFICATION = (
    ('DO', 'Osteopathic Doctor'),
    ('MD', 'Medical Doctor'),
)


class Review(models.Model):
    stars = models.IntegerField()
    review = models.CharField(max_length=500)
    title = models.CharField(max_length=25)


class Doctor(models.Model):
    certification = models.CharField(
        max_length=2,
        choices=CERTIFICATION,
        default=CERTIFICATION[0][0]
    )
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    contact = models.CharField(max_length=100)
    reviews = models.ManyToManyField(Review)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} is a {self.get_certification_display()} "

    def get_absolute_url(self):
        return reverse('detail', kwargs={'doctor_id': self.id})


class Photo(models.Model):
    url = models.CharField(max_length=200)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for cat_id: {self.doctor_id} @{self.url}"

    def get_absolute_url(self):
        return reverse('detail', kwargs={'doctor_id': self.id})
