# -*- coding: utf-8 -*-
from fastapi.encoders import jsonable_encoder
from starlette import status

from apps.people.models.people import People
from apps.people.serializers.people import PeopleOutSerializer
from core.test.transaction_test_case import TransactionTestCase


class ListPeopleTestCase(TransactionTestCase):
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
    def get_url():
        return '/api/v1/people/'

    def get_url_filtered_by_people_id(self):
        return '{}?{}'.format(self.get_url(), 'people_ids={}'.format(self.people1.id))

    def get_url_filtered_by_places_id(self):
        return '{}?{}'.format(self.get_url(), 'places_id={},{}'.format(self.people1.place_id, self.people2.place_id))

    def test_list_successfull(self):
        response = self.client.get(self.get_url())

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        payload = [PeopleOutSerializer(**people).dict() for people in response.json()]

        self.assertEqual(len(self.people) - 1, len(payload))

        for people in self.people:
            if not people.deleted_:
                people_obj_serialized = PeopleOutSerializer(**jsonable_encoder(people)).dict()
                self.assertIn(people_obj_serialized, payload)

    def test_list_filter_by_people_id_successfull(self):
        response = self.client.get(self.get_url_filtered_by_people_id())

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        payload = [PeopleOutSerializer(**people).dict() for people in response.json()]
        self.assertEqual(1, len(payload))

        for people in self.people:
            if people.id == self.people1.id:
                people_obj_serialized = PeopleOutSerializer(**jsonable_encoder(people)).dict()
                self.assertIn(people_obj_serialized, payload)

    def test_list_filter_by_places_id_successfull(self):
        response = self.client.get(self.get_url_filtered_by_places_id())

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        payload = [PeopleOutSerializer(**people).dict() for people in response.json()]
        self.assertEqual(2, len(payload))

        for people in self.people:
            if people.id == self.people1.id:
                people_obj_serialized = PeopleOutSerializer(**jsonable_encoder(people)).dict()
                self.assertIn(people_obj_serialized, payload)

    def test_list_order_successfull(self):
        response = self.client.get(self.get_url())

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        payload = [PeopleOutSerializer(**people).dict() for people in response.json()]
        self.assertEqual(len(self.people) - 1, len(payload))

        for people in self.people:
            if not people.deleted_:
                people_obj_serialized = PeopleOutSerializer(**jsonable_encoder(people)).dict()
                self.assertIn(people_obj_serialized, payload)
