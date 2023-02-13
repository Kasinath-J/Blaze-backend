from rest_framework import serializers
from .models import Profile

#Used for updating tasks regurlarly
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','name','leetcode', 'github', 'hackerrank', 'linkedin', 'codechef', 'codeforces']

