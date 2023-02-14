from rest_framework import serializers

from .models import OfficeBearer,Event

class EventSerializer(serializers.ModelSerializer):
    detail_date = serializers.SerializerMethodField() 
    class Meta:
        model = Event
        fields = '__all__'
    def get_detail_date(self,obj):
        return obj.date.strftime("%a %b %d %Y")

class OfficeBearerSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='profile.name')
    class Meta:
        model = OfficeBearer
        fields = ['name','position','img','rank','present_academic_year','officetype']

