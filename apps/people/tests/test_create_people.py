# -*- coding: utf-8 -*-
from fastapi.encoders import jsonable_encoder
from starlette import status

from apps.people.serializers.people import PeopleOutSerializer
from core.test.transaction_test_case import TransactionTestCase


class CreatePeopleTestCase(TransactionTestCase):

    @staticmethod
    def get_url():
        return '/api/v1/people/'

    def check_fields(self, people, response):
        payload = response.json()
        for key, value in people.items():
            self.assertEqual(value, payload.get(key))

    def test_create_kink_successfully(self):
        people = {
            'first_name': 'Kirigaya',
            'last_name': 'Kazuto',
            'place_id': 1,
            'is_king': True,
        }
        response = self.client.post(self.get_url(), json=people)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.check_fields(people, response)

    def test_create_duplicated_people(self):
        people = {
            'first_name': 'Kirigaya',
            'last_name': 'Kazuto',
            'place_id': 1,
            'is_king': False,
        }
        response = self.client.post(self.get_url(), json=people)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.check_fields(people, response)

        response = self.client.post(self.get_url(), json=people)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_duplicated_king(self):
        people = {
            'first_name': 'Kirigaya',
            'last_name': 'Kazuto',
            'place_id': 1,
            'is_king': True,
        }
        response = self.client.post(self.get_url(), json=people)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.check_fields(people, response)

        people['first_name'] = 'Asuna'
        people['last_name'] = 'Yuuki'
        response = self.client.post(self.get_url(), json=people)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_duplicated_king_non_alive(self):
        people = {
            'first_name': 'Kirigaya',
            'last_name': 'Kazuto',
            'place_id': 1,
            'is_king': True,
        }
        response = self.client.post(self.get_url(), json=people)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.check_fields(people, response)

        people['first_name'] = 'Asuna'
        people['last_name'] = 'Yuuki'
        people['is_alive'] = False
        response = self.client.post(self.get_url(), json=people)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
