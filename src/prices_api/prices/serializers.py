from rest_framework import serializers


class TestSerializer(serializers.Serializer):
    """Serializes two values for example"""

    a = serializers.IntegerField()
    b = serializers.IntegerField()


class CarInstanceSerializer(serializers.Serializer):
    kilometers = serializers.IntegerField()
    car_id = serializers.IntegerField()
    name = serializers.CharField(max_length=20)
    month = serializers.IntegerField()
    year = serializers.IntegerField()
