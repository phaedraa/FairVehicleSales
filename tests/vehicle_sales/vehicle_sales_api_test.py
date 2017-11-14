#!/usr/bin/env python
from django.conf import settings
settings.configure()

import django
django.setup()

import requests
import json
import unittest

# NOTE: These test can run using pytest, but running
# your local server via `./manage.py runserver` is first
# required as `nose` is not yet integrated.
# Also, ensure your test superuser has been created via
# python manage.py createsuperuser with username 'admin'
# and password 'password123'

URL = 'http://localhost:8000/vehicle_sales/'
HEADERS = {'Content-Type': 'application/json'}


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
    def setUp(self):
        self.auth = ('admin', 'password123')
        data = {
            'buyer': BUYERS[0],
            'price': 989898.33,
            'vin': VINS[0],
            'car_class': CAR_CLASSES[0],
            'seller': SELLERS[0],
        }
        # Not ideal solution. Better would be to get nose
        # integration working.
        res = requests.post(
            URL, data=json.dumps(data), headers=HEADERS, auth=self.auth)
        self.sale_id = res.json()['id']
        self.detail_url = '{}{}'.format(URL, self.sale_id)
        # self.created_sales = set()

    #def tearDown(self):
    #    for id in self.created_sales:
    #        sale = VehicleSales.objects.get(id=id)
    #        sale.delete()

    def test_vehicle_sales_post_invalid_buyer_seller_relationship(self):
        data = {
            'buyer': SELLERS[0],
            'price': 27990.00,
            'vin': VINS[0],
            'car_class': CAR_CLASSES[0],
            'seller': SELLERS[0],
        }
        res = requests.post(
            URL, data=json.dumps(data), headers=HEADERS, auth=self.auth)
        self.assertEqual(res.status_code, 400)

        data['buyer'] = BUYERS[0]
        data['seller'] = BUYERS[0]
        res = requests.post(
            URL, data=json.dumps(data), headers=HEADERS, auth=self.auth)
        self.assertEqual(res.status_code, 400)

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
                URL, data=json.dumps(data), headers=HEADERS, auth=self.auth)
            self.assertTrue(res.json() != {})
            self.assertEqual(res.status_code, 200)

            data = res.json()
            self.assertTrue(data['id'] not in ids)
            ids.add(data['id'])

            self.assertEqual(data['vin'], VINS[i])
            self.assertEqual(float(data['price']), price)
            self.assertEqual(data['buyer_type'], BUYERS[i]['type'])
            self.assertEqual(data['seller_type'], SELLERS[i]['type'])

            price += 12345.55
        # self.created_sales = ids

    def test_vehicle_sales_car_detail(self):
        for vin in VINS:
            get_url = '{}car/{}'.format(URL, vin)
            res = requests.get(
                get_url, data=json.dumps({'latest': True}),
                headers=HEADERS, auth=self.auth)
            self.assertTrue(res.json() != {})
            self.assertEqual(res.json().get('vin'), vin)

    def test_vehicle_sales_list_get(self):
        ids = set()
        for i in range(len(BUYERS)):
            data = {
                'buyer': BUYERS[i],
                'car_class': CAR_CLASSES[i],
                'seller': SELLERS[i],
                'latest': True
            }
            res = requests.get(
                URL, data=json.dumps(data), headers=HEADERS, auth=self.auth)

            self.assertEqual(res.status_code, 200)
            self.assertTrue(res.json() != {})

            sale_id = res.json()['id']
            self.assertTrue(sale_id not in ids)
            ids.add(sale_id)

    def test_vehicle_sales_detail_get(self):
        res = requests.get(self.detail_url, headers=HEADERS, auth=self.auth)
        self.assertEqual(res.json()['vin'], VINS[0])

    def test_vehicle_sales_detail_put(self):
        price = 99999.99
        res = requests.put(
            self.detail_url, data=json.dumps({'price': price}),
            headers=HEADERS, auth=self.auth)
        self.assertEqual(float(res.json()['price']), price)

    def test_vehicle_sales_detail_delete(self):
        res = requests.delete(self.detail_url, headers=HEADERS, auth=self.auth)
        self.assertTrue(res.json().get('Success') is not None)

if __name__ == '__main__':
    unittest.main()
