from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from bank_accounts.forms import BankAccountForm, CardFormSet
from bank_accounts.models import BankAccount


class BankAccountListView(LoginRequiredMixin, ListView):
    model = BankAccount
    template_name = 'bank_accounts/bank_account_list.html'
    context_object_name = 'bank_accounts'
    paginate_by = 12

    def get_queryset(self):
        queryset = BankAccount.objects.filter(user=self.request.user).order_by('name')

        account_id = self.request.GET.get('id')
        name = self.request.GET.get('name', '').strip()

        if account_id:
            queryset = queryset.filter(id=account_id)

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class BankAccountCreateView(LoginRequiredMixin, CreateView):
    model = BankAccount
    form_class = BankAccountForm
    template_name = 'bank_accounts/bank_account_form.html'
    success_url = reverse_lazy('bank_accounts:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['card_formset'] = CardFormSet(self.request.POST)
        else:
            data['card_formset'] = CardFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        card_formset = context['card_formset']
        if card_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            card_formset.instance = self.object
            card_formset.save()
            messages.success(self.request, 'Conta bancária e cartões criados com sucesso.')
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class BankAccountUpdateView(LoginRequiredMixin, UpdateView):
    model = BankAccount
    form_class = BankAccountForm
    template_name = 'bank_accounts/bank_account_form.html'
    success_url = reverse_lazy('bank_accounts:list')

    def get_queryset(self):
        return BankAccount.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['card_formset'] = CardFormSet(self.request.POST, instance=self.object)
        else:
            data['card_formset'] = CardFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        card_formset = context['card_formset']
        if card_formset.is_valid():
            self.object = form.save()
            card_formset.instance = self.object
            card_formset.save()
            messages.success(self.request, 'Conta bancária e cartões atualizados com sucesso.')
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class BankAccountDeleteView(LoginRequiredMixin, DeleteView):
    model = BankAccount
    template_name = 'bank_accounts/bank_account_confirm_delete.html'
    success_url = reverse_lazy('bank_accounts:list')

    def get_queryset(self):
        return BankAccount.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Conta bancária excluída com sucesso.')
        return super().delete(request, *args, **kwargs)