from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Problem

@api_view(['GET'])
def ProblemsEasyView(request):
    
    if request.method == 'GET':
        try:
            instance = Problem.objects.all()[0]
            return Response(instance.easy)
        
        except:
            try:
                instance = Problem(total_easy=614,total_medium=1335,total_hard=556,weekly_contest_no=323,biweekly_contest_no=93)
                instance.save()    
                return Response(instance["easy"])
            except:
                return Response(None)


@api_view(['GET'])
def ProblemsMediumView(request):
    if request.method == 'GET':
        try:
            instance = Problem.objects.all()[0]
            ret={}
            ret['medium'] = instance.medium
            ret['contest'] = instance.contest
            return Response(ret)
        
        except:
            try:
                instance = Problem(total_easy=614,total_medium=1335,total_hard=556,weekly_contest_no=323,biweekly_contest_no=93)
                instance.save()  
                ret={}
                ret['medium'] = instance.medium
                ret['contest'] = instance.contest
                return Response(ret)  
            except:
                return Response(None)


