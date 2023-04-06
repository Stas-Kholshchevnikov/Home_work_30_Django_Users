
from django.contrib import admin
from django.urls import path

import ads.views

urlpatterns = [
    path('', ads.views.CatListView.as_view()),
    path('<int:pk>/', ads.views.CatDetailView.as_view()),
    path('create/', ads.views.CatCreateView.as_view()),
    path('<int:pk>/update/', ads.views.CatUpdateView.as_view()),
    path('<int:pk>/delete/', ads.views.CatDeleteView.as_view()),
    ]
