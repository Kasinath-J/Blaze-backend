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
    class Meta:
        model = OfficeBearer
        fields = '__all__'
