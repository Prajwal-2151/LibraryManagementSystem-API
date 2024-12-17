from django.urls import path

from Book.views import BookAPI, BooksByAuthor, RecordAPI, GenerateReport, LatestReport

urlpatterns = [
          path('allbooks/', BookAPI.as_view({'get': 'list'})),
          path('bookdetails/<int:pk>/', BookAPI.as_view({'get': 'retrieve'})),
          path('addbook/', BookAPI.as_view({'post': 'create'})),
          path('updatebook/<int:pk>/', BookAPI.as_view({'put': 'update'})),
          path('partialupdatebook/<int:pk>/', BookAPI.as_view({'patch': 'partial_update'})),
          path('searchbook/', BookAPI.as_view({'get': 'search'})),
          path('deletebook/<int:pk>/', BookAPI.as_view({'delete': 'destroy'})),

          path('booksbyauthor/<int:a_id>/', BooksByAuthor.as_view()),

          path('borrow/', RecordAPI.as_view({'post': 'create'})),
          path('borrow/<int:pk>/return/', RecordAPI.as_view({'put': 'update'})),

          path('generate-report/', GenerateReport.as_view()),

          path('latest-report/', LatestReport.as_view()),

]
