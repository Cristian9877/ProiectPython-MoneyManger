import pat
from django.urls import path
from transaction import views
from transaction.views import display_user_balance

urlpatterns = [
    path('add_transaction/', views.TransactionCreateView.as_view(), name='add-transaction'),
    path('list_transactions/', views.TransactionListView.as_view(), name='list-transactions'),
    path('balance/',display_user_balance, name='balance'),
    path('send-transactions-email/', views.send_transactions_email, name='send-transactions-email'),
    path('update_transaction/<int:pk>', views.TransactionUpdateView.as_view(), name='update-transaction'),
    path('delete_transaction/<int:pk>/', views.TransactionDeleteView.as_view(), name='delete-transaction'),
    path('details_transaction/<int:pk>/', views.TransactionDetailView.as_view(), name='details-transaction'),

]