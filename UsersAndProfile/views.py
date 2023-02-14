from rest_framework import mixins,generics
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Profile
from .serializers import ProfileSerializer

import jwt
import time   

# For signing in
@api_view(['POST'])
def VerifyEmail(request):
    if request.method == 'POST':
        decoded = jwt.decode(request.data['credential'], options={"verify_signature": False})

        # If credentials expires after 1hr
        exp_time = decoded['exp']
        cur_time = int(time.time())
        if cur_time>exp_time:
            return Response(False)

        requested_email = decoded['email']
        send_Data = False
        try:
            # checking whether the requested email has a registereed account
            instance = Profile.objects.get(pk=requested_email)
            send_Data = True
        except:
            send_Data = False

        return Response(send_Data)



class ProfileList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):   

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# For updating profile details
class ProfileDetailPermission(BasePermission):
    message = 'Editing profile is restricted to the user and author only.'

    def has_object_permission(self, request, view, obj):
        
        if request.method in SAFE_METHODS:
            return True

        decoded = jwt.decode(request.headers['Authorization'].split(" ")[1], options={"verify_signature": False})
        actual_signed_user = decoded['email']
        
        # If credentials expires after 1hr
        exp_time = decoded['exp']
        cur_time = int(time.time())

        return (obj.id.email == actual_signed_user) and (cur_time<exp_time)

# For updating profile details
class ProfileDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.GenericAPIView):

    permission_classes = [ProfileDetailPermission]

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


@api_view(['GET'])
def EmailList(request):
    if request.method == 'GET':
        instance = Profile.objects.all()
        ret=[]
        for inst in instance:
            ret.append({"email":inst.id.email,
                        "year": inst.id.year})

        return Response(ret)
