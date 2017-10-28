from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from . import serializers
from . import price_utils
# Create your views here.


class UserPriceViewSet(viewsets.ViewSet):
    """API View for obtaining data about car and retriving price"""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.CarInstanceSerializer

    def list(self, request):
        """Message when get method is provided."""

        return Response({'message': 'Include car instance data'})

    def create(self, request):
        """Calculate values using test"""

        serializer = serializers.CarInstanceSerializer(data=request.data)

        if serializer.is_valid():
            answer = price_utils.get_car_name(serializer.data)
            message = 'The car is a {} from make {}'.format(answer['model'], answer['make'])

            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
