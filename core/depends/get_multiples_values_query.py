# -*- coding: utf-8 -*-
from fastapi import Query


def get_multiple_integer_values_query(label):
    def wrap(values: str = Query(None, regex = r'[1-9]+,?', alias = label)):
        if values:
            return [int(value) for value in values.split(',')]
        else:
            return []

    return wrap


def get_multiple_values_query(label):
    def wrap(values: str = Query(None, regex = r'[\w]+,?', alias = label)):
        if values:
            return values.split(',')
        else:
            return []

    return wrap
