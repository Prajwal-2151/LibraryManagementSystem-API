from django.urls import path

from Author.views import AuthorAPI

urlpatterns = [
          path('allauthors/', AuthorAPI.as_view({'get': 'list'})),
          path('authordetails/<int:pk>/', AuthorAPI.as_view({'get': 'retrieve'})),
          path('addauthor/', AuthorAPI.as_view({'post': 'create'})),
          path('updateauthor/<int:pk>/', AuthorAPI.as_view({'put': 'update'})),
          path('partialupdateauthor/<int:pk>/', AuthorAPI.as_view({'patch': 'partial_update'})),
          path('deleteauthor/<int:pk>/', AuthorAPI.as_view({'delete': 'destroy'})),

]
