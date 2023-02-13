from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins,generics

from .models import OfficeBearer,Event
from .serializers import OfficeBearerSerializer,EventSerializer

class OfficeBearerList(APIView):
    def get(self, request, format=None):
        instance = OfficeBearer.objects.all()
        serializer = OfficeBearerSerializer(instance, many=True)
        return Response(serializer.data)


class EventsList(mixins.ListModelMixin, generics.GenericAPIView):
# class Events(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Event.objects.all().order_by('-date')
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)