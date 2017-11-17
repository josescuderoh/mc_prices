from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from . import serializers
from . import helper
# Create your views here.


class UserPriceViewSet(viewsets.ViewSet):
    """API View for obtaining data about car and retriving price"""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.CarInstanceSerializer

    def list(self, request):
        """Message when get method is provided."""

        return Response({'message': 'Include car instance data'})

    def create(self, request):
        """Calculate used car price"""

        serializer = serializers.CarInstanceSerializer(data=request.data)

        if serializer.is_valid():
            # Create car instance
            car = helper.Car(**serializer.data)

            return Response(car.__dict__)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
