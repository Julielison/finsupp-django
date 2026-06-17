from rest_framework import serializers
from .models import Bill, BillItem


class BillItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillItem
        fields = ["id", "description", "amount", "transaction", "subscription_id", "created_at"]
        read_only_fields = ["id", "created_at"]


class BillSerializer(serializers.ModelSerializer):
    items = BillItemSerializer(many=True, required=False)

    class Meta:
        model = Bill
        fields = ["id", "account", "total", "status", "due_date", "paid_date", "description", "items", "created_at"]
        read_only_fields = ["id", "paid_date", "created_at"]

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        bill = Bill.objects.create(**validated_data)
        for it in items_data:
            BillItem.objects.create(bill=bill, **it)
        return bill

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        if items_data is not None:
            instance.items.all().delete()
            for it in items_data:
                BillItem.objects.create(bill=instance, **it)
        return instance
