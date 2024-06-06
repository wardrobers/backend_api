from typing import Any, Optional

from sqlalchemy import String, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import RelationshipProperty, aliased


class SearchMixin:
    """
    Provides robust and efficient search functionality, leveraging PostgreSQL's
    tsvector and tsquery for full-text searching and the Levenshtein library
    for optimized fuzzy matching.

    Supports:
        - Full-text search
        - Fuzzy search (using Levenshtein distance)
        - Search across multiple entities and relationships
        - Weighted search terms
        - Ranking of search results
    """

    model = None

    async def search(
        self,
        db_session: AsyncSession,
        search_term: str,
        fields: Optional[list[str]] = None,
        relationships: Optional[dict[str, tuple[str, Any]]] = None,
        weights: Optional[dict[str, float]] = None,
        fuzzy_threshold: int = 2,  # Maximum Levenshtein distance for fuzzy matches
        ranking: bool = False,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list:
        """
        Performs a comprehensive search across specified fields and relationships.

        Args:
            db_session (AsyncSession): The async database session.
            search_term (str): The term to search for.
            fields (Optional[List[str]]): A list of fields to search in the current entity.
            relationships (Optional[Dict[str, Tuple[str, Any]]]): A dictionary specifying relationships to search.
                Keys are relationship attributes on the model, values are tuples: (field_to_search, filter_value).
            weights (Optional[Dict[str, float]]): A dictionary assigning weights to search terms.
                Keys are search terms, values are their corresponding weights.
            fuzzy_threshold (int): Maximum Levenshtein distance for a fuzzy match.
            ranking (bool): Whether to enable result ranking based on relevance.
            limit (Optional[int]): Limit the number of results.
            offset (Optional[int]): Offset for pagination.

        Returns:
            list: A list of matching model instances, optionally ranked.
        """

        if not fields:
            fields = [
                column.name
                for column in self.model.__table__.columns
                if isinstance(column.type, String)
            ]

        search_query = select(self.model)

        # Full-text search and fuzzy search logic
        search_conditions = []
        for term, weight in (weights or {"": 1.0}).items():
            vector = func.to_tsvector(
                "english", func.concat(*[getattr(self.model, field) for field in fields])
            )
            query = func.plainto_tsquery("english", term)
            search_conditions.append(
                vector.match(query, postgresql_regconfig="english")
            )

            # Use Levenshtein.distance for fuzzy matching
            if fuzzy_threshold > 0:
                for field in fields:
                    search_conditions.append(
                        func.funcfilter(
                            func.levenshtein(
                                func.lower(getattr(self.model, field)), func.lower(term)
                            ),
                            lambda dist: dist <= fuzzy_threshold,
                        )
                    )

        search_query = search_query.where(or_(*search_conditions))

        # Relationship search logic
        if relationships:
            for rel_attr, (rel_field, rel_filter) in relationships.items():
                relationship: RelationshipProperty = getattr(self.model, rel_attr)
                related_self = relationship.mapper.class_
                rel_alias = aliased(related_self)
                search_query = search_query.join(rel_alias, relationship).filter(
                    getattr(rel_alias, rel_field) == rel_filter
                )

                search_conditions = []
                vector = func.to_tsvector(
                    "english", func.concat(*[getattr(rel_alias, rel_field)])
                )
                query = func.plainto_tsquery("english", search_term)
                search_conditions.append(vector.match(query))

                if fuzzy_threshold > 0:
                    search_conditions.append(
                        func.funcfilter(
                            func.levenshtein(
                                func.lower(getattr(self.model, field)), func.lower(term)
                            ),
                            lambda dist: dist <= fuzzy_threshold,
                        )
                    )

                search_query = search_query.where(or_(*search_conditions))

        # Ranking logic (using a simplified ranking approach for demonstration)
        if ranking:
            rank = func.ts_rank_cd(
                func.setweight(
                    func.to_tsvector("english", func.coalesce(self.model.name, "")), "A"
                )
                | func.setweight(
                    func.to_tsvector("english", func.coalesce(self.model.description, "")),
                    "B",
                ),
                func.plainto_tsquery("english", search_term),
            )
            search_query = search_query.order_by(rank.desc())

        if limit:
            search_query = search_query.limit(limit)
        if offset:
            search_query = search_query.offset(offset)

        async with db_session.begin():
            result = await db_session.execute(search_query)
            return result.scalars().all()
