from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table

import db


class Author(db.Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))


class Deployment(db.Base):
    __tablename__ = 'deployment'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('author.id'))
    module_id = Column(Integer, ForeignKey('module.id'))
    occured_at = Column(DateTime)


module_tag_table = Table('module_tag', db.Base.metadata,
                         Column('module_id', Integer, ForeignKey('module.id')),
                         Column('right_id', Integer, ForeignKey('tag.id')))


class Module(db.Base):
    __tablename__ = 'module'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))


class Tag(db.Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
