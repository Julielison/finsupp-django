from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from .models import Bill
from .services import BillService


class BillListView(LoginRequiredMixin, ListView):
    model = Bill
    template_name = 'bills/bill_list.html'
    context_object_name = 'bills'
    paginate_by = 20

    def get_queryset(self):
        qs = Bill.objects.filter(account__user=self.request.user).order_by('due_date')
        status = self.request.GET.get('status')
        # 'ALL' means no status filter
        if status and status != 'ALL':
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status_filter'] = self.request.GET.get('status', 'ALL')
        return ctx


class BillDetailView(LoginRequiredMixin, DetailView):
    model = Bill
    template_name = 'bills/bill_detail.html'
    context_object_name = 'bill'

    def post(self, request, *args, **kwargs):
        # handle pay action
        self.object = self.get_object()
        if 'pay' in request.POST:
            try:
                BillService.pay_bill(self.object, request.user)
                messages.success(request, 'Fatura paga com sucesso.')
            except Exception as exc:
                messages.error(request, f'Erro ao pagar fatura: {exc}')
        return redirect(reverse('bills:detail', args=[self.object.pk]))
