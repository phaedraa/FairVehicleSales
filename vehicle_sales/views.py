import json
from django.db.models import Q

from car_classes.models import CarClass
from .models import VehicleSales
from .serializers import VehicleSalesSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from rest_framework.response import Response
from .vehicle_sales_utils import (
    fetch_entity,
    fetch_or_create_entity,
    validate_buyer_seller_relationship,
)


def fetch_or_create_buyer_and_seller(data):
    buyer_data = data.pop('buyer')
    seller_data = data.pop('seller')
    validate_buyer_seller_relationship(buyer_data, seller_data)
    return (
        fetch_or_create_entity(buyer_data),
        fetch_or_create_entity(seller_data))


def update_data_with_buyer_seller_info(data, buyer, seller):
    data['buyer_id'] = buyer.id
    data['seller_id'] = seller.id
    data['buyer_type'] = buyer.type()
    data['seller_type'] = seller.type()


def fetch_or_create_related_classes_and_update_data(data):
    buyer, seller = fetch_or_create_buyer_and_seller(data)
    update_data_with_buyer_seller_info(data, buyer, seller)


@api_view(['GET'])
def vehicle_sales_car_detail(request, vin):
    """ Get all Vehicle Sales of specific car """ 
    try:
    	vehicle_sales = VehicleSales.objects.filter(vin=vin).order_by('created_at')
    	return_latest = request.data.get('latest')
    	serializer = (
    	    VehicleSalesSerializer(vehicle_sales.first()) if return_latest else
    	    VehicleSalesSerializer(vehicle_sales, many=True))
    	return Response(serializer.data)
    except Exception as e:
    	error = {'error': 'Invalid request: {}'.format(str(e))}
    	return Response(error, status.HTTP_400_BAD_REQUEST)


def fetch_car_classes(data):
    if not data:
        return None
    query = Q()    
    if data.get('make'):
        query &= Q(make=data.get('make'))
    if data.get('model'):
        query &= Q(model=data.get('model'))
    if data.get('year'):
        query &= Q(year=data.get('year'))
    return CarClass.objects.filter(query)


@api_view(['GET', 'POST'])
def vehicle_sales_list(request):
    """ Query Vehicle Sales by car_class, buyer, and/or seller or, Create Vehicle Sale """
    if request.method == 'GET':
        data = request.data
        vehicle_sales = VehicleSales.objects.filter().order_by('created_at')
        try:
            car_classes = fetch_car_classes(data.get('car_class'))
            if car_classes:
                vehicle_sales = vehicle_sales.filter(car_class__in=car_classes)
        except Exception as e:
            error = {'error': 'Invalid car_class query: {}'.format(str(e))}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        try:
        	validate_buyer_seller_relationship(data.get('buyer'), data.get('seller'))
        except Exception as e:
        	return Response(error, status=status.HTTP_400_BAD_REQUEST)

        try:
            buyer = fetch_entity(data.get('buyer'))
            if buyer:
                vehicle_sales = vehicle_sales.filter(Q(buyer_id=buyer.id, buyer_type=buyer.type()))
        except Exception as e:
            error = {'error': 'Invalid buyer query: {}'.format(str(e))}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        try:
            seller = fetch_entity(data.get('seller'))
            if seller:
                vehicle_sales = vehicle_sales.filter(Q(seller_id=seller.id, seller_type=seller.type()))
        except Exception as e:
            error = {'error': 'Invalid seller query: {}'.format(str(e))}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        return_latest = data.get('latest')
        serializer = (
            VehicleSalesSerializer(vehicle_sales, many=True) if not return_latest
            else VehicleSalesSerializer(vehicle_sales.first()))
        return Response(serializer.data)


    if request.method == 'POST':
    	data = request.data
        try:
        	fetch_or_create_related_classes_and_update_data(data)
        except Exception as e:
        	error = {'error': 'Invalid buyer-seller data: {}'.format(str(e))}
        	return Response(error, status=status.HTTP_400_BAD_REQUEST)

        try:
        	vehicle_sale = VehicleSales.create_sale(data)
    		serializer = VehicleSalesSerializer(vehicle_sale)
        	return Response(serializer.data)
        except Exception as e:
        	error = {'error': 'Invalid request data: {}'.format(str(e))}
        	return Response(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def vehicle_sales_detail(request, sale_id):
    """
    Retrieve, update or delete a vehicle sale.
    """
    try:
        vehicle_sale = VehicleSales.objects.get(id=sale_id)
    except vehicle_sale.DoesNotExist:
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VehicleSalesSerializer(vehicle_sale)
        return Response(serializer.data)

    if request.method == 'PUT':
        try:
            VehicleSales.update_data(vehicle_sale, request.data)
            serializer = VehicleSalesSerializer(vehicle_sale)
            return Response(serializer.data)
        except Exception as e:
            error = {'error': 'Invalid request data: {}'.format(str(e))}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        try:
            vehicle_sale.delete()
            data = {
                'Success': 'Vehicle Sale {} successfully deleted'.format(sale_id),
            }
            return Response(data)
        except Exception as e:
            error = {'error': 'Invalid request: {}'.format(str(e))}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

