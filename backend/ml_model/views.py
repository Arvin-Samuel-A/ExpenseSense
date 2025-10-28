from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .predict import predict_category
from .serializers import ClassifyExpenseSerializer, ClassifyExpenseResponseSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def classify_expense(request):
    """
    POST /ml/classify/
    
    Classify expense category from SMS text using CNN model
    
    Request body:
    {
        "sms_text": "Spent Rs 500 at Cafe Coffee Day"
    }
    
    Response:
    {
        "category": "food",
        "confidence": 0.95,
        "all_probabilities": {...},
        "preprocessed_text": "..."
    }
    """
    serializer = ClassifyExpenseSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    sms_text = serializer.validated_data['sms_text']
    
    # Get prediction
    result = predict_category(sms_text)
    
    # Check for errors
    if 'error' in result:
        return Response(
            {'error': result['error'], 'category': result['category']},
            status=status.HTTP_200_OK  # Still return 200 with fallback category
        )
    
    # Serialize response
    response_serializer = ClassifyExpenseResponseSerializer(result)
    
    return Response(
        response_serializer.data,
        status=status.HTTP_200_OK
    )
