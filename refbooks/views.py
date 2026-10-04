from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import RefBook
from .serializers import (
    RefBookSerializer,
    RefBookElementSerializer,
)


class RefBookListAPIView(APIView):
    def get(self, request):
        date_param = request.query_params.get("date")
        

        refbooks = RefBook.objects.all()

        if date_param:
            try:
                requested_date = parse_date(date_param)
            except ValueError:
                return Response(
                    {"detail": "Параметр date должен быть в формате ГГГГ-ММ-ДД."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if requested_date is None:
                return Response(
                    {
                        "detail": (
                            "Параметр date должен быть "
                            "в формате ГГГГ-ММ-ДД."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            refbooks = refbooks.filter(
                versions__start_date__isnull=False,
                versions__start_date__lte=requested_date,
            ).distinct()

        serializer = RefBookSerializer(refbooks, many=True)

        return Response(
            {
                "refbooks": serializer.data,
            }
        )

class RefBookElementsAPIView(APIView):
    def get(self, request, pk):
        try:
            refbook = RefBook.objects.get(pk=pk)
        except RefBook.DoesNotExist:
            return Response(
                {
                    "detail":"Справочник не найден."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        version_name = request.query_params.get("version")

        if version_name:
            version = refbook.versions.filter(
                version=version_name,
            ).first()

            if version is None:
                return Response(
                    {
                        "detail": "Указанная версия справочника не найдена."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            version = refbook.get_current_version()

            if version is None:
                return Response(
                    {
                        "detail": "Для справочника нет актуальной версии"
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

        elements = version.elements.all()

        serializer = RefBookElementSerializer(
            elements,
            many=True,
        )

        return Response (
            {
                "detail": serializer.data,
            }
        )