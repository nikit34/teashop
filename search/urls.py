from django.urls import path

from .views import SearchProductView, rag_ask_view

urlpatterns = [
  path('', SearchProductView.as_view(), name='query'),
  path('ask/', rag_ask_view, name='ask'),
 ]
