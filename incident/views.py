from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serialilizers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
import random
from django.http import Http404

# Create your views here.

class SignUpAPIView(APIView):
    """ 
        This view is used for the create user
    """
    def post(self, request, format=None):
        
        try:
            data = request.data
            email = data.get('email',None)
            first_name = data.get('first_name',None)
            last_name = data.get('last_name',None)
            phone_number = data.get('phone_number',None)
            password = data.get('password', None)
            
            params = {
                'email':email,
                'first_name':first_name,
                'last_name':last_name,
                'phone_number':phone_number,
                'password':password,
            }
            serializer = UserSignUpSerializers(data=params)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                user.set_password(serializer.data['password'])
                user.save()
            else:
                return Response({"status":False, "msg":str(serializer.error_messages)})
            
            return Response({'status':True,'message':"User hass been created Successfully"}, status=201)
        except Exception as val_err:
            return Response({'staus':False,'message':str(val_err)})


class LoginAPIView(APIView):
    """ 
        This API is used for login user
    """
    
    def post(self, request, formate = None):
        
        try:
            data = request.data
            email = data.get('email',None)
            password = data.get('password', None)
            
            user = authenticate(email= email, password = password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({'status':True,'refresh':str(refresh),"access":str(refresh.access_token)})
            return Response({'status':False})
        
        except Exception as val_err:
            return Response({'status':False,'message':str(val_err)})
        
        
class CreateIncidentAPIView(APIView):
    """ 
        This API is used for create incident
    """ 
    permission_classes = (IsAuthenticated, )
    
    def post(self, request, formate=None):
        try:
            user = request.user
            data = request.data
            incident_details = data.get('incident_details', None)
            priority = data.get('priority', None)
            incident_status = data.get('incident_status', None)
            now = datetime.now()
            year = now.year
            num = random.randint(11111,99999)
            incident_number = f"RMG-{str(num)}{str(year)}"
                        
            params = {
                'incident_number':incident_number,
                'reporter_name':user.id,
                'reported_datetime':now,
                'incident_details':incident_details,
                'priority':priority,
                'incident_status':incident_status,
            }
            serializer = IncidentCreateAPISerializers(data=params)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                return Response({'status':False})
            return Response({'status':True,'message':f"Incident is create sucessfully--{user.first_name}"})
        except Exception as val_err:
            return Response({'status':False,'error':str(val_err)})
    
    
class GetncidentDetailsView(APIView):
    """ 
        This API is used for GET incident Details user wise specific user incident_details
    """
    permission_classes = (IsAuthenticated,)    
    
    def get(self, request):
        user = request.user
        queryset = IncidentDetails.objects.filter(reporter_name=user.id)
        serializer = IncidentDetailsSerializers(queryset, many=True)
        return Response({'status': True, 'data': serializer.data})
        
    
class GetUpdateIncidentDetails(APIView):
    """
        Retrieve or update  incident details.
    """
    permission_classes = (IsAuthenticated, )
    
     
    def get_object(self, pk):
        try:
            return IncidentDetails.objects.get(pk=pk, reporter_name=self.request.user)
        except IncidentDetails.DoesNotExist:
            raise Http404 

    def get(self, request, pk, format=None):
        incident = self.get_object(pk)
        serializer = IncidentDetailsSerializers(incident)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        try:
            incident = IncidentDetails.objects.get(incident_status="Resolve")
            return Response({"status": True,'message': f"This incident is already cloased {incident.incident_number}"})
        except:
            incident_obj = self.get_object(pk)
            serializer = IncidentDetailsSerializers(incident_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
  
class SearchIncidentAPIView(APIView):
    
    permission_classes = (IsAuthenticated, )
    
    def post(self,request):
        try:
            incident_number = request.data.get('incident_number')
            incident_obj = IncidentDetails.objects.get(incident_number=incident_number)
            serializer = IncidentDetailsSerializers(incident_obj)
            return Response({'status': True, 'data': serializer.data}, status=200)
        except Exception as val_error:
            return Response({'status': False, 'msg': "Incident_number is not found",'error': str(val_error)})