from django.urls import path

from em_project.orders import views

urlpatterns = [
    path('', views.OrderIndexView.as_view(), name='orders'),
]
