from datetime import datetime

import pytz
from sqlalchemy import select, delete

from src.facade.database.errors import RequestedFilterNotAllowedError


class QueryMixin:
    _OPERATORS = {'in', 'not_in'}
    _MODEL = None
    _database_facade = None

    def _get_filters(self, fields: set) -> set:
        return {f"{field}__{operator}" for field in fields for operator in self._OPERATORS}

    def _check_requested_filters(self, requested_filter_keys: set, fields: set) -> None:
        diff = requested_filter_keys - self._get_filters(fields)
        if diff:
            diff = sorted(list(diff))
            raise RequestedFilterNotAllowedError(diff)

    def generate_select_query(self, *, filters: dict, entity_fields: set):
        self._check_requested_filters(requested_filter_keys=set(filters.keys()), fields=entity_fields)
        model_fields = self._get_repository_fields(entity_fields=entity_fields)

        query = select(model_fields)

        query = self._generate_filters(query=query, filters=filters)
        return query

    def generate_delete_query(self, *, filters: dict):
        self._check_requested_filters(requested_filter_keys=set(filters.keys()), fields=entity_fields)

        query = delete()

        query = self._generate_filters(query=query, filters=filters)
        return query

    def _generate_filters(self, *, query, filters: dict):
        for query_filter in filters:
            field, operator = query_filter.split('__')
            repository_field = self._get_repository_field(entity_field=field)

            # TODO: sqlalchemy bool_op is not working as I expected.
            if operator == 'in':
                query = query.where(repository_field.in_(filters[query_filter]))
            elif operator == 'not_in':
                query = query.where(~repository_field.in_(filters[query_filter]))
            else:
                raise RequestedFilterNotAllowedError(operator)

        return query

    def _get_repository_fields(self, *, entity_fields: set) -> set:
        return {self._get_repository_field(entity_field=entity_field) for entity_field in entity_fields}

    def _get_repository_field(self, *, entity_field: str):
        return getattr(self._MODEL, entity_field)

    @staticmethod
    def fix_datetime_without_timezone(data: dict) -> dict:
        # FIXME: Set all dates to utc, SQLAlchemy bug with SQLite
        for key in data:
            if type(data[key]) == datetime:
                data[key] = pytz.utc.localize(data[key])

        return data
