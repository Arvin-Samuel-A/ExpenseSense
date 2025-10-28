from django.urls import path
from .views import classify_expense

urlpatterns = [
    path('classify/', classify_expense, name='classify-expense'),
]
