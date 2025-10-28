from django.apps import AppConfig


class MlModelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ml_model'
    verbose_name = 'ML Model'
    
    def ready(self):
        """Load ML model when Django starts"""
        from .load_model import load_expense_model
        try:
            load_expense_model()
            print("✓ ML Model loaded successfully")
        except Exception as e:
            print(f"✗ Failed to load ML model: {e}")
