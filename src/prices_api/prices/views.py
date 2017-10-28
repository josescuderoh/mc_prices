from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from . import serializers
from . import tests
# Create your views here.


class UserPriceViewSet(viewsets.ViewSet):
    """API View for obtaining data about car and retriving price"""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.TestSerializer

    def list(self, request):
        """Message when get method is provided."""

        return Response({'message': 'Include values a and b'})

    def create(self, request):
        """Calculate values using test"""

        serializer = serializers.TestSerializer(data=request.data)

        if serializer.is_valid():
            answer = tests.calculate_answer(serializer.data)
            message = 'The result is {}'.format(answer)

            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
