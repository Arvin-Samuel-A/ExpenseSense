from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'category', 'merchant', 'payment_mode', 'date', 'created_at')
    list_filter = ('category', 'payment_mode', 'date', 'created_at')
    search_fields = ('user__email', 'merchant', 'notes', 'sms_raw_text')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'
    ordering = ('-date',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'amount', 'merchant', 'category', 'payment_mode')
        }),
        ('Date & Time', {
            'fields': ('date',)
        }),
        ('Additional Information', {
            'fields': ('sms_raw_text', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
