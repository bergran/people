# -*- coding: utf-8 -*-
from fastapi.encoders import jsonable_encoder
from starlette import status

from apps.people.models import People
from apps.people.serializers.people import PeopleOutSerializer
from core.test.transaction_test_case import TransactionTestCase


class DeletePeopleTestCase(TransactionTestCase):

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

    def test_delete_kink_successfully(self):
        people_obj = self.people1

        response = self.client.delete(self.get_url(people_obj.id))

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_kink_remove_deleted_people(self):
        people_obj = self.people3
        response = self.client.delete(self.get_url(people_obj.id))

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_delete_non_exists_people(self):
        people_obj = self.people3

        response = self.client.delete(self.get_url(people_obj.id + 1))

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
