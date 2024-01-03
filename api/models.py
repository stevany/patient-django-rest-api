import uuid
from django.db import models
from datetime import datetime

# Create your models here.
class Gender(models.TextChoices):
    FEMALE = "FEMALE"
    MALE = "MALE"

class Patient(models.Model):
  id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
  firstName = models.CharField(max_length=30)
  lastName = models.CharField(max_length=50)
  dob = models.CharField(max_length=10)
  gender = models.CharField(
      choices=Gender.choices,
      max_length=6
  )
  phoneNumber = models.CharField(max_length=16)
  createdAt = models.DateTimeField(auto_now_add=True)
  updatedAt = models.DateTimeField(auto_now_add=True)

  class Meta:
    db_table="patient"
    ordering= ['-createdAt']



class Address(models.Model):
  id = models.UUIDField(primary_key=True,default=uuid.uuid4)
  patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
  street = models.CharField(max_length=200)
  suburb = models.CharField(max_length=100)
  state = models.CharField(max_length=100)
  postcode = models.CharField(max_length=20)

  class Meta:
    db_table="address"
  

