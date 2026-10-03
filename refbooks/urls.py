from django.urls import path

from .views import RefBookListAPIView


urlpatterns = [
    path(
        "refbooks/",
        RefBookListAPIView.as_view(),
        name="refbook-list",
    ),
]