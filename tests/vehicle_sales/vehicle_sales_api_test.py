#!/usr/bin/env python
from django.conf import settings
settings.configure()

import django
django.setup()

import requests
import json
import unittest

URL = 'http://localhost:8000/vehicle_sales/'
HEADERS = {'Content-Type': 'application/json'}
AUTH = ('admin', 'password123')


VINS = [
    '1234567890123AVC1',
    '12345678BDC234581',
    '12345678YYY234581',
    '1234567OPK1234581'
]
BUYERS = [
    {'ein': '553598', 'type': 'dealer', 'id': '', 'name': 'DealerABC'},
    {'first_name': 'Alisia', 'last_name': 'Sanchez', 'ssn_last_4': '8932',
        'dob': '05/30/1967', 'license_no': '123ND5', 'type': 'individual',
        'id': ''},
    {'ein': '555592', 'type': 'dealer', 'id': '', 'name': 'Dealer999'},
    {'first_name': 'Irene', 'last_name': 'Maldovia', 'ssn_last_4': '8891',
        'dob': '05/30/1937', 'license_no': '123NZ5', 'type': 'individual',
        'id': ''},
]
SELLERS = [
    {'first_name': 'Jose', 'last_name': 'Sanchez', 'ssn_last_4': '8931',
        'dob': '05/30/1947', 'license_no': '123AC5', 'type': 'individual',
        'id': ''},
    {'ein': '555591', 'type': 'dealer', 'id': '', 'name': 'Dealer123'},
    {'first_name': 'Leo', 'last_name': 'B', 'ssn_last_4': '8934',
        'dob': '05/30/1977', 'license_no': '123NC5', 'type': 'individual',
        'id': ''},
    {'ein': '555593', 'type': 'dealer', 'id': '', 'name': 'Dealer3099'},
]
CAR_CLASSES = [
    {'make': 'Tesla', 'model': 'S3', 'year': '2017'},
    {'make': 'Nissan', 'model': 'Leaf', 'year': '2015'},
    {'make': 'Jaguar', 'model': 'ZeroE', 'year': '2017'},
    {'make': 'Tesla', 'model': 'T1000', 'year': '2015'},
]


class VehicleSalesAPITests(unittest.TestCase):
    def test_vehicle_sales_post_invalid_buyer_seller_relationship(self):
        data = {
            'buyer': SELLERS[0],
            'price': 27990.00,
            'vin': VINS[0],
            'car_class': CAR_CLASSES[0],
            'seller': SELLERS[0],
        }
        res = requests.post(
            URL, data=json.dumps(data), headers=HEADERS, auth=AUTH)
        assert res.status_code == 400

        data['buyer'] = BUYERS[0]
        data['seller'] = BUYERS[0]
        res = requests.post(
            URL, data=json.dumps(data), headers=HEADERS, auth=AUTH)
        assert res.status_code == 400

    def test_vehicle_sales_post_requests(self):
        price = 10000.00
        ids = set()
        for i in range(len(BUYERS)):
            data = {
                'buyer': BUYERS[i],
                'price': price,
                'vin': VINS[i],
                'car_class': CAR_CLASSES[i],
                'seller': SELLERS[i]
            }
            res = requests.post(
                URL, data=json.dumps(data), headers=HEADERS, auth=AUTH)
            assert res.json()
            assert res.status_code == 200

            data = res.json()
            assert data['id'] not in ids
            ids.add(data['id'])

            assert data['vin'] == VINS[i]
            assert float(data['price']) == price
            assert data['buyer_type'] == BUYERS[i]['type']
            assert data['seller_type'] == SELLERS[i]['type']

            price += 12345.55

    def test_vehicle_sales_get_by_car_requests(self):
        for vin in VINS:
            get_url = '{}car/{}'.format(URL, vin)
            res = requests.get(
                get_url, data=json.dumps({'latest': True}),
                headers=HEADERS, auth=AUTH)
            assert res.json()
            assert res.json().get('vin') == vin

    def test_vehicle_sales_get_requests(self):
        ids = set()
        for i in range(len(BUYERS)):
            data = {
                'buyer': BUYERS[i],
                'car_class': CAR_CLASSES[i],
                'seller': SELLERS[i],
                'latest': True
            }
            res = requests.get(
                URL, data=json.dumps(data), headers=HEADERS, auth=AUTH)

            self.assertEqual(res.status_code, 200)
            assert res.json()

            sale_id = res.json()['id']
            assert sale_id not in ids
            ids.add(sale_id)


if __name__ == '__main__':
    unittest.main()
