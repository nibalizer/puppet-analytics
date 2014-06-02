from sqlalchemy.exc import IntegrityError

from models import Author, Deployment, Module, Tag


def get_all_authors(session):
    return session.query(Author).all()


def get_all_modules(session):
    return session.query(Module).all()


def get_all_deployments(session):
    return session.query(Deployment).\
        join(Deployment.author).\
        join(Deployment.module).\
        join(Deployment.tags).all()


def get_deployments_by_module(session, module_name):
    return session.query(Deployment).\
        join(Deployment.author).\
        join(Deployment.module).\
        join(Deployment.tags).\
        filter(Module.name == module_name).all()


def get_deployments_by_author_module(session, author_name, module_name):
    return session.query(Deployment).\
        join(Deployment.author).\
        join(Deployment.module).\
        join(Deployment.tags).\
        filter(Author.name == author_name).\
        filter(Module.name == module_name).all()


def insert_or_get_model(session, model, index_key, index_value):
    inst = model(index_value)
    session.add(inst)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return session.query(model).filter(index_key == index_value).one()
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

    deployment = Deployment(author.id, module.id, occured_at)
    session.add(deployment)
    deployment.tags = tags
    session.commit()
    return deployment
