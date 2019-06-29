# -*- coding: utf-8 -*-
from fastapi.encoders import jsonable_encoder
from starlette import status

from apps.people.models import People
from apps.people.serializers.people import PeopleOutSerializer
from core.test.transaction_test_case import TransactionTestCase


class CreatePeopleTestCase(TransactionTestCase):

    def setUp(self):
        self.people1 = People(first_name='Kirigaya', last_name='Kazuto', place_id=1)
        self.people2 = People(first_name='Asuna', last_name='Yuuki', place_id=2)
        self.people3 = People(first_name='Sinon', last_name='Asada', deleted_=True, place_id=3)

        self.create_models()

    def create_models(self):
        self.people = [self.people1, self.people2, self.people3]

        self.session.add_all(self.people)
        self.session.commit()
        self.refresh_models()

    def refresh_models(self):
        for people in self.people:
            self.session.refresh(people)

    @staticmethod
    def get_url(pk):
        return '/api/v1/people/{}'.format(pk)

    def check_fields(self, people, response):
        payload = response.json()
        for key, value in people.items():
            self.assertEqual(value, payload.get(key))

    def test_update_kink_successfully(self):
        people_obj = self.people1

        people = {
            'first_name': '{} updated'.format(people_obj.first_name),
            'last_name': '{} updated'.format(people_obj.last_name),
            'place_id': 1,
            'is_king': True,
        }

        response = self.client.put(self.get_url(people_obj.id), json=people)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.check_fields(people, response)

    def test_update_kink_duplicated_first_name(self):
        people_obj = self.people1

        people = {
            'first_name': self.people2.first_name,
            'last_name': '{} updated'.format(people_obj.last_name),
            'place_id': 1,
            'is_king': False,
        }

        response = self.client.put(self.get_url(people_obj.id), json=people)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_update_kink_duplicated_king(self):
        people_obj = self.people1

        people = {
            'first_name': self.people2.first_name,
            'last_name': '{} updated'.format(people_obj.last_name),
            'place_id': 2,
            'is_king': True,
        }

        response = self.client.put(self.get_url(people_obj.id), json=people)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
