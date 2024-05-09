from sqlalchemy.orm import Session


class BulkActionsMixin:
    @classmethod
    def bulk_create(cls, db_session: Session, items: list[dict]) -> None:
        instances = [cls(**item) for item in items]
        db_session.bulk_save_objects(instances)
        db_session.flush()
        return instances
    
    @classmethod
    def bulk_insert(cls, db_session: Session, items: list[dict], return_defaults: bool = False):
        """
        Perform bulk inserts efficiently.
        """
        db_session.bulk_insert_mappings(cls, items, return_defaults=return_defaults)
        db_session.flush()

    @classmethod
    def bulk_update(cls, db_session: Session, items: list[dict]):
        """
        Perform bulk updates efficiently.
        """
        db_session.bulk_update_mappings(cls, items)
        db_session.flush()

    @classmethod
    def bulk_delete(cls, db_session: Session, ids: list):
        """
        Perform bulk deletes efficiently.
        """
        db_session.query(cls).filter(cls.id.in_(ids)).delete(synchronize_session='fetch')
        db_session.flush()
