from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Expense
from .serializers import (
    ExpenseSerializer, 
    ExpenseCreateSerializer,
    ExpenseSummaryResponseSerializer
)


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Expense CRUD operations
    
    list: GET /expenses/ - Get all expenses for authenticated user
    create: POST /expenses/ - Create a new expense
    retrieve: GET /expenses/{id}/ - Get a specific expense
    update: PUT /expenses/{id}/ - Update an expense
    partial_update: PATCH /expenses/{id}/ - Partially update an expense
    destroy: DELETE /expenses/{id}/ - Delete an expense
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ExpenseCreateSerializer
        return ExpenseSerializer
    
    def get_queryset(self):
        """Return expenses for the authenticated user only"""
        user = self.request.user
        queryset = Expense.objects.filter(user=user)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by payment mode
        payment_mode = self.request.query_params.get('payment_mode', None)
        if payment_mode:
            queryset = queryset.filter(payment_mode=payment_mode)
        
        return queryset.order_by('-date')
    
    def perform_create(self, serializer):
        """Set the user when creating an expense"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'], url_path='summary/monthly')
    def monthly_summary(self, request):
        """
        GET /expenses/summary/monthly/
        
        Get monthly expense summary grouped by category
        Query params: month (1-12), year (YYYY)
        If not provided, uses current month/year
        """
        # Get month and year from query params or use current
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        
        now = timezone.now()
        
        if month and year:
            try:
                month = int(month)
                year = int(year)
            except ValueError:
                return Response(
                    {'error': 'Invalid month or year format'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            month = now.month
            year = now.year
        
        # Get expenses for the specified month/year
        expenses = Expense.objects.filter(
            user=request.user,
            date__year=year,
            date__month=month
        )
        
        # Calculate total
        total_amount = expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        total_count = expenses.count()
        
        # Group by category
        category_summary = expenses.values('category').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')
        
        # Calculate percentages
        by_category = []
        for item in category_summary:
            percentage = (item['total'] / total_amount * 100) if total_amount > 0 else 0
            by_category.append({
                'category': item['category'],
                'total': item['total'],
                'count': item['count'],
                'percentage': round(percentage, 2)
            })
        
        # Prepare response
        response_data = {
            'month': datetime(year, month, 1).strftime('%B'),
            'year': year,
            'total_amount': total_amount,
            'total_expenses': total_count,
            'by_category': by_category
        }
        
        serializer = ExpenseSummaryResponseSerializer(response_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='summary/yearly')
    def yearly_summary(self, request):
        """
        GET /expenses/summary/yearly/
        
        Get yearly expense summary
        Query params: year (YYYY)
        """
        year = request.query_params.get('year')
        
        if year:
            try:
                year = int(year)
            except ValueError:
                return Response(
                    {'error': 'Invalid year format'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            year = timezone.now().year
        
        expenses = Expense.objects.filter(
            user=request.user,
            date__year=year
        )
        
        total_amount = expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        total_count = expenses.count()
        
        # Monthly breakdown
        monthly_data = []
        for month in range(1, 13):
            month_expenses = expenses.filter(date__month=month)
            month_total = month_expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
            monthly_data.append({
                'month': datetime(year, month, 1).strftime('%B'),
                'total': month_total,
                'count': month_expenses.count()
            })
        
        return Response({
            'year': year,
            'total_amount': total_amount,
            'total_expenses': total_count,
            'monthly_breakdown': monthly_data
        }, status=status.HTTP_200_OK)
