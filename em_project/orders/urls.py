from django.urls import path
from em_project.orders import views

urlpatterns = [
    path('', views.OrderIndexView.as_view(),
         name='orders'),
    path('create/', views.OrderCreateView.as_view(),
         name='create_order'),
    path('delete/', views.OrderDeleteView.as_view(),
         name='delete_order'),
    path('<int:pk>/', views.OrderView.as_view(), name='view_order'),
    path('<int:pk>/delete/',
         views.DeleteOrderByIDView.as_view(), name='delete_order_by_id'),
    path('<int:pk>/status/',
         views.OrderEditStatusView.as_view(), name='edit_status'),
    path('<int:pk>/edit/',
         views.OrderItemsEditView.as_view(), name='edit_order_items'),
    path('income/', views.CalculateIncomeView.as_view(),
         name='income'),
]
