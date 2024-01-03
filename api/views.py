from rest_framework import status
from rest_framework.views import APIView,Response
from django.core.serializers import serialize
from .models import Address,Gender,Patient
from .serializers import AddressSerializer,PatientSerializer
from datetime import datetime
import json
import uuid

# Create your views here.
class PatientAPI(APIView):
  def get(self,request):
    serialize_class = PatientSerializer
    patients = Patient.objects.all()
    patient_list = []
    patientSerializer = PatientSerializer(patients, many=True).data
    for patient in patientSerializer:
      addresses = Address.objects.filter(patient=patient.get("id"))
      if addresses is None:
        patient_data = patient
      else:  
        addressSerializer = AddressSerializer(addresses,many=True).data
        patient_data = patient
        patient_data['address'] = addressSerializer[0]

      patient_list.append(patient_data)
    return Response({"data": patient_list}, status=status.HTTP_200_OK)

  def post(self,request):
    firstName = request.data.get("firstName")
    lastName = request.data.get("lastName")
    gender = Gender[request.data.get("gender")]
    dob = request.data.get("dob")
    phoneNumber = request.data.get("phoneNumber")
    street = request.data.get("street")
    suburb = request.data.get("suburb")
    state = request.data.get("state")
    postcode = request.data.get("postcode")

    patientSerializer = PatientSerializer(data={
      "firstName": firstName,
      "lastName": lastName,
      "gender": gender,
      "dob": dob,
      "phoneNumber": phoneNumber
    })

    if patientSerializer.is_valid():
      patientSerializer.save()
      request.data['patient'] = patientSerializer.data['id']
      addressSerializer = AddressSerializer(data=request.data)
      if addressSerializer.is_valid():
        addressSerializer.save()
        data = patientSerializer.data
        data['address'] = addressSerializer.data
        response_data = {"data": data }
      else:
        response_data = {"message": {"address": addressSerializer.errors }}

    else:
      response_data = {"message": {"patient": patientSerializer.errors }}
    return Response(response_data, status=status.HTTP_200_OK)

  def put(self,request,id):
    print('put')
    firstName = request.data.get("firstName")
    lastName = request.data.get("lastName")
    gender = Gender[request.data.get("gender")]
    dob = request.data.get("dob")
    phoneNumber = request.data.get("phoneNumber")
    street = request.data.get("street")
    suburb = request.data.get("suburb")
    state = request.data.get("state")
    postcode = request.data.get("postcode")
    

    patient = Patient.objects.get(id=id)
    address = Address.objects.filter(patient__id=id).first()

    patient_data = {"firstName": firstName, "gender": gender, "dob": dob, "phoneNumber": phoneNumber}
    if patient is None or address is None:
      response_data = "Patient or Address is not exist"
    else:
      patientSerializer = PatientSerializer(patient,data=request.data, partial=True)
 

      if patientSerializer.is_valid():
        addressSerializer = AddressSerializer(address,data=request.data, partial=True) 
        patientSerializer.validated_data['updatedAt'] = datetime.now()

        patientSerializer.save()
        if addressSerializer.is_valid():
          addressSerializer.save()
      
        response_data = patientSerializer.data
        response_data.address = addressSerializer.data
      else:
        response_data = "Faield to save!"  

    return Response({"data": response_data }, status=status.HTTP_200_OK)

  def delete(self,request,id):
    print()
    patient = Patient.objects.filter(id=id).first()
    address = Address.objects.filter(patient=id).first()
    if patient is None or address is None:
        response_data = "Patient or Address is not exist"
    else:
      patient.delete()
      address.delete()
      response_data = id

    return Response({"data": response_data }, status=status.HTTP_200_OK)
      


