from django.urls import path
from main import views

urlpatterns = [
    # path('funFact', views.DidYouKnowView.as_view()),
    path('waste-category', views.WasteCategoryView.as_view()),
    path('environmental_tip', views.EnvironmentalTipView.as_view())
]
