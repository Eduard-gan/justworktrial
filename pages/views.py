from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView

from pages.models import Page
from pages.serializers import PageListSerializer, PageDetailSerializer
from tasks import update_page_content_counters


class PageListView(ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageListSerializer
    permission_classes = [permissions.IsAuthenticated]


class PageDetailView(RetrieveAPIView):
    queryset = Page.objects.all()
    serializer_class = PageDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        data = super().retrieve(request, *args, **kwargs)
        update_page_content_counters.delay(page_id=data.data['id'])
        return data
