from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from transactions.forms import TransactionForm
from transactions.models import Transaction

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 12

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user).order_by('-date', '-id')
        
        description = self.request.GET.get('description', '').strip()
        if description:
            queryset = queryset.filter(description__icontains=description)
            
        return queryset

class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Transação criada com sucesso.')
        return super().form_valid(form)

class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:list')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Transação atualizada com sucesso.')
        return super().form_valid(form)

class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    success_url = reverse_lazy('transactions:list')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Transação excluída com sucesso.')
        return super().delete(request, *args, **kwargs)
