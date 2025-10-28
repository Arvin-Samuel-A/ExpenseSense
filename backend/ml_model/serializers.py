from rest_framework import serializers


class ClassifyExpenseSerializer(serializers.Serializer):
    """Serializer for expense classification input"""
    sms_text = serializers.CharField(required=True, max_length=1000)
    
    def validate_sms_text(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("SMS text cannot be empty")
        return value.strip()


class ClassifyExpenseResponseSerializer(serializers.Serializer):
    """Serializer for expense classification response"""
    category = serializers.CharField()
    confidence = serializers.FloatField()
    all_probabilities = serializers.DictField(child=serializers.FloatField())
    preprocessed_text = serializers.CharField(required=False)
    error = serializers.CharField(required=False)
