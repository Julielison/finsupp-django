from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Bill
from .serializers import BillSerializer
from .services import BillService
from .exceptions import BillAlreadyPaid, BillNotFound, BillPaymentError


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all().order_by('-due_date')
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # limit to user's accounts unless staff
        if user.is_staff:
            return super().get_queryset()
        return self.queryset.filter(account__user=user)

    @action(detail=True, methods=['patch'], url_path='pay')
    def pay(self, request, pk=None):
        bill = self.get_object()
        # ownership check
        if not (request.user.is_staff or bill.account.user == request.user):
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        try:
            tx = BillService.pay_bill(bill, paid_by_user=request.user)
        except BillAlreadyPaid:
            return Response({"detail": "Bill already paid."}, status=status.HTTP_409_CONFLICT)
        except BillPaymentError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": "Internal error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"success": True, "transaction_id": getattr(tx, 'id', None)})
