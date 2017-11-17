from rest_framework import serializers


class TestSerializer(serializers.Serializer):
    """Serializes two values for example"""

    a = serializers.IntegerField()
    b = serializers.IntegerField()


class CarInstanceSerializer(serializers.Serializer):
    car_id = serializers.IntegerField()
    kilometers = serializers.IntegerField()
    model_year = serializers.IntegerField()
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    state = serializers.IntegerField()
