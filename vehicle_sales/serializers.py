import serpy
from .models import VehicleSales
from car_classes.serializers import CarClassSerializer


class VehicleSalesSerializer(serpy.Serializer):
    seller_id = serpy.IntField()
    seller_type = serpy.Field()
    buyer_id = serpy.IntField()
    buyer_type = serpy.Field()
    car_class = serpy.Field()
    vin = serpy.Field()
    price = serpy.FloatField()
    created_at = serpy.Field()
    id = serpy.IntField()
    car_class = serpy.MethodField()


    def get_car_class(self, obj):
        serialized = CarClassSerializer(obj.car_class)
        return serialized.data
