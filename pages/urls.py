from django.urls import path, include
from pages.views import PageListView, PageDetailView


urlpatterns = [
    path('pages/', PageListView.as_view(), name='list-pages'),
    path('pages/<int:pk>/', PageDetailView.as_view(), name='page-detail'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]
