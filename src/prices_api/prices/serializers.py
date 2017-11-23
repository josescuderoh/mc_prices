from rest_framework import serializers


class TestSerializer(serializers.Serializer):
    """Serializes two values for example"""

    a = serializers.IntegerField()
    b = serializers.IntegerField()


class CarInstanceSerializer(serializers.Serializer):
    car_id = serializers.IntegerField()  # Always required
    kilometers = serializers.IntegerField()     # Always required
    model_year = serializers.IntegerField()     # Always required
    year = serializers.IntegerField(required=False)  # Only if RUNT register is sent
    month = serializers.IntegerField(required=False)      # Only if RUNT register is sent
    state = serializers.IntegerField(required=False)  # Always required

    def get_validation_exclusions(self):
        exclusions = super(CarInstanceSerializer, self).get_validation_exclusions()
        return exclusions + ['month', 'year', 'status']
