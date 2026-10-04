from django.urls import path

from .views import (
    RefBookElementsAPIView,
    RefBookListAPIView,
)

urlpatterns = [
    path(
        "refbooks/",
        RefBookListAPIView.as_view(),
        name="refbook-list",
    ),
    path(
        "refbooks/<int:pk>/elements/",
        RefBookElementsAPIView.as_view(),
        name="refbook-elements",
    )
]