from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from decorators.execption_handler import execption_hanlder
from api.service import AiParkService
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin

aipark_service = AiParkService()

class AiParkView(APIView):
    def post(self, request, *args, **kwargs):
        return create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return get_list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return delete_project(request, *args, **kwargs)

class TextUpdateView(GenericAPIView, UpdateModelMixin):
    def put(self, request, *args, **kwargs):
        return partial_update(request, *args, **kwargs)

@execption_hanlder()
@parser_classes([JSONParser])
def create(request, *args, **kwargs):
    datas = request.data
    return JsonResponse(aipark_service.create(datas), status=status.HTTP_201_CREATED, safe=False)

@execption_hanlder()
@parser_classes([JSONParser])
def get_list(request, *args, **kwargs):
    project_id = kwargs.get("project_id")
    page = request.GET.get("page", 1)
    serailizer, context = aipark_service.get_list(project_id, page)
    return JsonResponse({"page":context, "data": serailizer }, status=status.HTTP_200_OK, safe=False)

@execption_hanlder()
@parser_classes([JSONParser])
def partial_update(request, *args, **kwargs):
    data = request.data
    project_id = kwargs["project_id"]
    index= kwargs["index"]
    kwargs['partial'] = True
    partial = kwargs.pop('partial', False)
    return JsonResponse(aipark_service.update(data, project_id, index, partial), status=status.HTTP_200_OK)

@execption_hanlder()
@parser_classes([JSONParser])
def delete_project(request, *args, **kwargs):
    project_id = kwargs["project_id"]
    return JsonResponse(aipark_service.delete(project_id), status=status.HTTP_204_NO_CONTENT, safe=False)