from sqlalchemy import func, or_
from sqlalchemy import String


class SearchMixin:
    @classmethod
    def search(cls, db_session, search_term, fields=None, filters=None, facets=None):
        """
        Performs full-text search with filtering and faceted search capabilities.
        """
        if not fields:
            fields = [
                column.name
                for column in cls.__table__.columns
                if isinstance(column.type, String)
            ]

        vector = func.to_tsvector(
            "english", func.concat(*[getattr(cls, field) for field in fields])
        )
        query = func.plainto_tsquery("english", search_term)

        search_query = db_session.query(cls).filter(vector.match(query))

        if filters:
            for field, value in filters.items():
                search_query = search_query.filter(getattr(cls, field) == value)

        if facets:
            facet_counts = {}
            for facet_field in facets:
                facet_results = (
                    db_session.query(getattr(cls, facet_field), func.count(cls.id))
                    .group_by(getattr(cls, facet_field))
                    .all()
                )
                facet_counts[facet_field] = {
                    result[0]: result[1] for result in facet_results
                }
            return search_query, facet_counts

        return search_query
