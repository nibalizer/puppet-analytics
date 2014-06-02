from sqlalchemy.exc import IntegrityError

from models import Author, Module, Tag


def get_author_by_name(session, author_name):
    return session.query(Author).filter(Author.name == author_name).one()


def insert_or_get_model(session, model, index_key, index_value):
    inst = model(index_value)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return session.query(Author).filter(index_key == index_value).one()
    return inst


def insert_or_get_author(session, author_name):
    return insert_or_get_model(session, Author, Author.name, author_name)


def insert_or_get_module(session, module_name):
    return insert_or_get_model(session, Module, Module.name, module_name)


def insert_or_get_tag(session, tag):
    return insert_or_get_model(session, Tag, Tag.value, tag)


def insert_or_get_tags(session, tags):
    return [insert_or_get_tag(session, x) for x in tags]


def insert_raw_deployment(session, author_name, module_name, tags, occured_at):
    # TODO:greghaynes This could make a lot less round trips to the DB
    author = insert_or_get_author(session, author_name)
    module = insert_or_get_module(session, module_name)
    tags = insert_or_get_tags(session, tags)
