# -*- coding: utf-8 -*-
from fastapi.encoders import jsonable_encoder
from starlette import status

from apps.people.models.people import People
from apps.people.serializers.people import PeopleOutSerializer
from core.test.transaction_test_case import TransactionTestCase


class RetrievePeopleTestCase(TransactionTestCase):
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

    def test_retrieve_deleted(self):
        people = self.people3
        response = self.client.get(self.get_url(people.id))

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_retrieve_people1(self):
        people = self.people1
        response = self.client.get(self.get_url(people.id))

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        people_serialized = PeopleOutSerializer(**jsonable_encoder(people)).dict()
        people_response_serialized = PeopleOutSerializer(**response.json()).dict()
        self.assertEqual(people_serialized, people_response_serialized)

    def test_retrieve_people2(self):
        people = self.people2
        response = self.client.get(self.get_url(people.id))

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        people_serialized = PeopleOutSerializer(**jsonable_encoder(people)).dict()
        people_response_serialized = PeopleOutSerializer(**response.json()).dict()
        self.assertEqual(people_serialized, people_response_serialized)

    def test_retrieve_people_non_exist(self):
        people = self.people3
        response = self.client.get(self.get_url(people.id + 1))

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)