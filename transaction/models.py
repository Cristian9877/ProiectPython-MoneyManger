from django.db import models
from django.contrib.auth.models import User  # Import the User model

# Define the choices for transaction type
TRANSACTION_TYPES = (
    ('income', 'Income'),
    ('expense', 'Expense'),
)
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link transaction to a user
    amount = models.IntegerField()
    details = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=255, choices=TRANSACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Returns a string representation of the Transaction object
    def __str__(self):
        return f'{self.transaction_type.capitalize()} - {self.amount} for {self.user.username}'




