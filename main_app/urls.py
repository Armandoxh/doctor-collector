from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('doctors/<int:doctor_id>/add_photo/',
         views.add_photo, name='add_photo'),
    path('doctors/', views.doctor_index, name="index"),
    path('doctors/<int:doctor_id>/', views.doctor_detail, name='detail'),
    path('doctors/create/', views.DoctorCreate.as_view(), name='doctor_create'),
    path('doctors/<int:pk>/update/',
         views.DoctorUpdate.as_view(), name='doctor_update'),
    path('doctors/<int:pk>/delete/',
         views.DoctorDelete.as_view(), name='doctor_delete'),
    path('doctors/<int:doctor_id>/add_photo/',
         views.add_photo, name='add_photo')
]
