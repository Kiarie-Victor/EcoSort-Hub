from django.urls import path
from main import views

urlpatterns = [
    path('api/funFact', views.DidYouKnowView.as_view())
]
