from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LCDSerializer,GHDSerializer,LIDSerializer,HRDSerializer,CCDSerializer,CFDSerializer

from .models import LeetcodeDetail,GithubDetail,LinkedInDetail,HackerrankDetail,CodechefDetail,CodeforcesDetail


class LeetcodeList(APIView):
    def get(self, request, format=None):
        instance = LeetcodeDetail.objects.all()
        serializer = LCDSerializer(instance, many=True)
        return Response(serializer.data)

class GithubList(APIView):
    def get(self, request, format=None):
        instance = GithubDetail.objects.all()
        serializer = GHDSerializer(instance, many=True)
        return Response(serializer.data)

class LinkedInList(APIView):
    def get(self, request, format=None):
        instance = LinkedInDetail.objects.all()
        serializer = LIDSerializer(instance, many=True)
        return Response(serializer.data)

class HackerrankList(APIView):
    def get(self, request, format=None):
        instance = HackerrankDetail.objects.all()
        serializer = HRDSerializer(instance, many=True)
        return Response(serializer.data)

class CodechefList(APIView):
    def get(self, request, format=None):
        instance = CodechefDetail.objects.all()
        serializer = CCDSerializer(instance, many=True)
        return Response(serializer.data)

class CodeForcesList(APIView):
    def get(self, request, format=None):
        instance = CodeforcesDetail.objects.all()
        serializer = CFDSerializer(instance, many=True)
        return Response(serializer.data)

