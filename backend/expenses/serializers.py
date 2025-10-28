from rest_framework import serializers
from .models import Expense
from django.utils import timezone


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Serializer for Expense model
    """
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Expense
        fields = [
            'id', 
            'user', 
            'user_email',
            'amount', 
            'merchant', 
            'category',
            'payment_mode',
            'date', 
            'sms_raw_text',
            'notes',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
    
    def validate_amount(self, value):
        """Validate amount is positive"""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value
    
    def validate_date(self, value):
        """Validate date is not in the future"""
        if value > timezone.now():
            raise serializers.ValidationError("Date cannot be in the future")
        return value


class ExpenseCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating expenses (user is set automatically)
    """
    
    class Meta:
        model = Expense
        fields = [
            'amount', 
            'merchant', 
            'category',
            'payment_mode',
            'date', 
            'sms_raw_text',
            'notes'
        ]
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value


class MonthlySummarySerializer(serializers.Serializer):
    """
    Serializer for monthly expense summary
    """
    category = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    count = serializers.IntegerField()
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)


class ExpenseSummaryResponseSerializer(serializers.Serializer):
    """
    Response serializer for expense summary endpoint
    """
    month = serializers.CharField()
    year = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_expenses = serializers.IntegerField()
    by_category = MonthlySummarySerializer(many=True)
