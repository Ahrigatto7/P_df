from sqlalchemy.orm import Session
from .models import DataItem


def create_document(session: Session, title, doc_type, content, meta):
    doc = DataItem(title=title, doc_type=doc_type, content=content, meta=meta)
    session.add(doc)
    session.commit()
    return doc


def update_document(session: Session, doc_id, **kwargs):
    doc = session.query(DataItem).get(doc_id)
    for k, v in kwargs.items():
        setattr(doc, k, v)
    session.commit()
    return doc


def delete_document(session: Session, doc_id):
    doc = session.query(DataItem).get(doc_id)
    session.delete(doc)
    session.commit()
    return True


def list_documents(session: Session, doc_type=None):
    q = session.query(DataItem)
    if doc_type:
        q = q.filter(DataItem.doc_type == doc_type)
    return q.all()

