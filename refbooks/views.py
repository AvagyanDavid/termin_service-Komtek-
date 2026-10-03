from datetime import date

from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import RefBook
from .serializers import RefBookSerializer

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