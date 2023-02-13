from django.contrib import admin
from .models import LeetcodeDetail,GithubDetail,LinkedInDetail,HackerrankDetail,CodechefDetail,CodeforcesDetail

# Register your models here.
admin.site.register(LeetcodeDetail)
admin.site.register(GithubDetail)
admin.site.register(LinkedInDetail)
admin.site.register(HackerrankDetail)
admin.site.register(CodechefDetail)
admin.site.register(CodeforcesDetail)