from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DeleteView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.views.generic.edit import UpdateView


from transaction.forms import TransactionForm, TransactionUpdateForm
from transaction.models import Transaction


def calculate_user_balance(user):
    total_income = Transaction.objects.filter(user=user, transaction_type='income').aggregate(total=Sum('amount'))[
                       'total'] or 0
    total_expenses = Transaction.objects.filter(user=user, transaction_type='expense').aggregate(total=Sum('amount'))[
                         'total'] or 0

    balance = total_income - total_expenses
    is_positive = balance >= 0

    return {
        'balance': balance,
        'is_positive': is_positive
    }


class TransactionCreateView(LoginRequiredMixin, CreateView):
    template_name = 'transaction/add_transaction.html'
    model = Transaction
    form_class = TransactionForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionListView(LoginRequiredMixin, ListView):
    template_name = 'transaction/list_of_transactions.html'
    model = Transaction
    context_object_name = 'all_transactions'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        balance_data = calculate_user_balance(self.request.user)
        context['balance'] = balance_data['balance']
        context['is_positive'] = balance_data['is_positive']
        return context

class TransactionUpdateView(LoginRequiredMixin,UpdateView):
    template_name = 'transaction/update_transaction.html'
    model = Transaction
    form_class = TransactionUpdateForm
    success_url = '/list_transactions/'

class TransactionDeleteView(LoginRequiredMixin,DeleteView):
    template_name = 'transaction/delete_transaction.html'
    model = Transaction
    success_url = '/list_transactions/'

class TransactionDetailView(DetailView):
    template_name = 'transaction/details_transaction.html'
    model = Transaction

@login_required
def create_transaction(request):
    if request.method == 'POST':
        try:

            amount = request.POST.get('amount')
            details = request.POST.get('details')
            date = request.POST.get('date')
            transaction_type = request.POST.get('transaction_type')

            if not (amount and details and date and transaction_type):
                return HttpResponseBadRequest("All fields are required.")

            Transaction.objects.create(
                user=request.user,
                amount=amount,
                details=details,
                description=date,
                transaction_type=transaction_type
            )

            return redirect('transaction_success')

        except Exception as e:

            print(f"Error occurred: {e}")
            return HttpResponseBadRequest("An error occurred while processing the transaction.")

    return render(request, 'transaction/add_transaction.html')


@login_required
def send_transactions_email(request):
    if request.method == 'POST':
        user = request.user

        # Check if the user has an email address
        recipient_email = user.email
        if not recipient_email:
            messages.error(request,
                           "You do not have an email address associated with your account. Please update your email and try again.")
            return redirect(reverse('balance'))

        # Validate the email address format
        try:
            validate_email(recipient_email)
        except ValidationError:
            messages.error(request, "Your email address is invalid. Please update your email and try again.")
            return redirect(reverse('balance'))

        # Fetch transactions and balance data
        transactions = Transaction.objects.filter(user=user)
        balance_data = calculate_user_balance(user)

        # Prepare transaction details for the email
        transaction_details = "\n".join(
            [f"Date: {t.created_at}, Amount: {t.amount}, Description: {t.description}" for t in transactions]
        )

        # Compose email subject and message
        email_subject = "Your Transactions and Account Balance"
        email_message = (
            f"Hello {user.username},\n\n"
            f"Here is the summary of your account:\n"
            f"Balance: {balance_data['balance']}\n\n"
            f"Transactions:\n{transaction_details or 'No transactions found.'}\n\n"
            "Thank you for using MoneyManager!"
        )

        # Try to send the email
        try:
            emails_sent = send_mail(
                email_subject,
                email_message,
                'yoyoma988@gmail.com',  # Replace with your verified sender email
                [recipient_email],
                fail_silently=False,
            )

            # Check if the email was successfully sent
            if emails_sent > 0:
                messages.success(request,
                                 "Email with your transactions and balance has been sent to your email address.")
            else:
                messages.error(request, "Email could not be sent. Please try again.")

        except Exception as e:
            # Log and display a generic error message
            print(f"An error occurred while sending the email: {e}")
            messages.error(request, "An unexpected error occurred while sending the email. Please try again later.")

        return redirect(reverse('balance'))


# Function-Based View to Show Balance
@login_required
def display_user_balance(request):
    balance_data = calculate_user_balance(request.user)

    return render(request, 'transaction/balance.html', {
        'balance': balance_data['balance'],
        'is_positive': balance_data['is_positive']
    })
