from .models import IpRecord
from rest_framework import serializers


class TraceSerializer(serializers.Serializer):
    ip = serializers.IPAddressField()
    name = serializers.CharField()
    code = serializers.CharField()
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    currency_code = serializers.CharField(write_only=True)
    currencies = serializers.SerializerMethodField()
    distance_to_uy = serializers.FloatField(read_only=True)

    def get_currencies(self, obj):
        return obj.country.currencies

    def create(self, validated_data):
        ip = validated_data.pop('ip')
        lat = validated_data.pop('lat')
        lon = validated_data.pop('lon')
        new_ip_obj = IpRecord.objects.create_with_country(
            country_data=validated_data,
            ip=ip,
            lat=lat,
            lon=lon
        )
        return new_ip_obj
