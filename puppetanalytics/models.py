from sqlalchemy import (Column,
                        DateTime,
                        ForeignKey,
                        Integer,
                        String,
                        Table)
from sqlalchemy.orm import relationship

import db


class Author(db.Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __init__(self, name):
        self.name = name


deployment_tag_table = Table('deployment_tag', db.Base.metadata,
                             Column('module_id',
                                    Integer,
                                    ForeignKey('deployment.id')),
                             Column('right_id', Integer, ForeignKey('tag.id')))


class Deployment(db.Base):
    __tablename__ = 'deployment'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('author.id'))
    module_id = Column(Integer, ForeignKey('module.id'))
    occured_at = Column(DateTime)
    author = relationship("Author")
    module = relationship("Module")
    tags = relationship("Tag", secondary=deployment_tag_table)

    def __init__(self, author_id, module_id, occured_at):
        self.author_id = author_id
        self.module_id = module_id
        self.occured_at = occured_at


class Module(db.Base):
    __tablename__ = 'module'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    def __init__(self, name):
        self.name = name


class Tag(db.Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    value = Column(String(50), unique=True)

    def __init__(self, value):
        self.value = value
