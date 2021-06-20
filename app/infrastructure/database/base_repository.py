# coding=utf-8
"""
Base Repository
"""
import logging

from sqlalchemy import not_
from sqlalchemy.orm import lazyload
from sqlalchemy.orm.exc import NoResultFound

from app import extensions

logger = logging.getLogger(__name__)


def handle_database_exception(exception):
    pass


class BaseRepository(object):
    """
        Base repository
    """

    def __init__(self, db=None):
        self.db = db or extensions.db

    def session(self):
        """
        returns session
        :return:
        """
        return self.db.session

    def flush_session(self):
        try:
            self.session().flush()
        except Exception as exp:
            handle_database_exception(exp)

    def _bulk_save_or_update(self, items):
        try:
            self.session().bulk_save_objects(items)
        except Exception as exp:
            handle_database_exception(exp)

    def _save(self, item):
        """
        :param item:
        :return:
        """
        try:
            self.session().add(item)
        except Exception as exp:
            handle_database_exception(exp)
        return item

    def _update(self, item):
        """
        :param item:
        :return:
        """
        try:
            self.session().merge(item)
        except Exception as exp:
            handle_database_exception(exp)
        return item

    def _update_all(self, items):
        """
        updates multiple items
        :param items:
        :return:
        """
        for item in items:
            self.session().merge(item)
        return items

    def _bulk_update_mappings(self, model, mapping_dicts):
        if not mapping_dicts:
            return
        try:
            self.session().bulk_update_mappings(model, mapping_dicts)
        except Exception as exp:
            handle_database_exception(exp)

    def _bulk_insert_mappings(self, model, mapping_dicts):
        if not mapping_dicts:
            return
        try:
            self.session().bulk_insert_mappings(model, mapping_dicts)
        except Exception as exp:
            handle_database_exception(exp)

    def _save_all(self, items):
        """
        updates multiple items
        :param items:
        :return:booking
        """
        self.session().add_all(items)
        return items

    def filter(self, model, *queries, for_update=False, nowait=True):
        """
        :param model:
        :param queries:
        :param for_update:
        :param nowait:
        :return:
        """
        queryset = self.session().query(model)
        queryset = queryset.filter(*queries)
        if for_update:
            queryset = queryset.with_for_update(nowait=nowait)
        return queryset

    def exclude(self, query, *exclude_queries):
        real_excludes = [not_(ex) for ex in exclude_queries]
        return query.filter(*real_excludes)

    def filter_by_join(self, models, join_clause, *queries):
        """
        :param models:
        :param join_clause:
        :param queries:
        :return:
        """
        queryset = self.session().query(*models).filter(join_clause)
        items = queryset.filter(*queries)
        return items

    def get(self, model, **queries):
        """

        :param model:
        :param queries:
        :return:
        """
        queryset = self.session().query(model)

        for attr, value in queries.items():
            if value:
                value = "%s" % value
            queryset = queryset.filter(getattr(model, attr) == value)
        try:
            return queryset.one()
        except NoResultFound:
            return None
        except Exception as exp:
            handle_database_exception(exp)

    def get_for_update(self, model, nowait=True, **queries):
        """
        The query will lock the row that is returned.
        If the transaction cannot lock the row (which will happen when some other transactions have obtained the lock),
        then:
            - If `nowait=True`, the query will fail with error
            - If `nowait=False`, the query will wait for the lock to get released.

        :param model:
        :param nowait:
        :param queries:
        :return:
        """
        queryset = self.session().query(model)
        for attr, value in queries.items():
            if value:
                value = "%s" % value
            queryset = queryset.filter(getattr(model, attr) == value)

        # Forcing lazy load here because
        # https://www.postgresql.org/message-id/21634.1160151923@sss.pgh.pa.us
        queryset = queryset.options(lazyload("*"))
        try:
            return queryset.with_for_update(nowait=nowait).one()
        except NoResultFound:
            return None
        except Exception as exp:
            handle_database_exception(exp)

    def delete(self, item):
        """
        delete item
        :param item:
        :return:booking
        """
        self.session().delete(item)

    def query(self, *model):
        return self.session().query(*model)
