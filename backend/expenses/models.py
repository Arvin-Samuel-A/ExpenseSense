from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()


class Expense(models.Model):
    """
    Expense model to store user expense transactions
    """
    
    CATEGORY_CHOICES = [
        ('food', 'Food & Dining'),
        ('transport', 'Transportation'),
        ('shopping', 'Shopping'),
        ('entertainment', 'Entertainment'),
        ('bills', 'Bills & Utilities'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('groceries', 'Groceries'),
        ('travel', 'Travel'),
        ('other', 'Other'),
    ]
    
    PAYMENT_MODE_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('netbanking', 'Net Banking'),
        ('wallet', 'Wallet'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='expenses',
        db_index=True
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    merchant = models.CharField(max_length=255, blank=True)
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES,
        default='other',
        db_index=True
    )
    payment_mode = models.CharField(
        max_length=50,
        choices=PAYMENT_MODE_CHOICES,
        default='other'
    )
    date = models.DateTimeField(db_index=True)
    sms_raw_text = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'expenses'
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
        ordering = ['-date']
        indexes = [
            models.Index(fields=['user', '-date']),
            models.Index(fields=['user', 'category']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.amount} - {self.category} - {self.date}"
