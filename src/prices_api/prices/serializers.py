from rest_framework import serializers


class TestSerializer(serializers.Serializer):
    """Serializes two values for example"""

    a = serializers.IntegerField()
    b = serializers.IntegerField()
