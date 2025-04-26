from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Table,
    ForeignKey,
)  # modules for db operations
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    relationship,
    Mapped,
    mapped_column,
)  # object-relational mapper (ORM) - bridge between OOP amd relational dbs
import datetime as dt
from typing import List, Optional


Base = declarative_base()  # any class that inheirts from Base is considered a SQLAlchemy ORM model - parent class

engine = create_engine(
    'sqlite:///./tasks.db', echo=True
)  # connect to the database, and enable logging of all the statements

sessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # factory for database sessions (managing connections) -> ensure transactions are not automatically comitted


class Task(Base):
    """
    Define the Task class as a child of the Base class - It is an ORM Model
    Class maps to the 'tasks' table in the database
    """

    __tablename__ = 'tasks'  # table name

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(
        nullable=False
    )  # field, title, which is a string and required
    description: Mapped[Optional[str]] = mapped_column(
        nullable=True
    )  # field, description, which is a string
    status: Mapped[Optional[str]] = mapped_column(
        default='to-do'
    )  # field, status, which is a string and default as 'to-do'
    dueDate: Mapped[Optional[dt.datetime]] = mapped_column(
        nullable=True
    )  # field, dueDate, which is a datetime object
    createdAt: Mapped[dt.datetime] = mapped_column(
        default=dt.datetime.now
    )  # field, createdAt, which is a DateTime object and default as current time
    updatedAt: Mapped[dt.datetime] = mapped_column(
        default=dt.datetime.now, onupdate=dt.datetime.now
    )  # field, updatedAt, which is a DateTime object and defaults and updates as current time

    tags: Mapped[List['Tag']] = relationship(
        'Tag', secondary='task_tags', back_populates='tasks'
    )  # defines a many to many relationship with the 'Tag' model
    # 'secondary'=task_tags: specifies the association table and tells SQLAlchemy where to look for these connections
    # 'back_populates'=tasks: tells to create a 'tasks' attribute on the 'Tag' model that will contain a list of tasks associated with the tags. (i.e urgent.tasks will give a list of urgent tasks). This is creating the reverse side of the relationship for easy navigation 
    # this allows us to have a field, tags, in the 'Task' model, that will behave like a Python list. But, in actual db, the field is managed by the association table w/ foreign keys.


    def __repr__(self):
        """
        Defines how an instance of the Task class should be represented as a string, for logging
        """
        return f'<Task(id={self.id}, title={self.title}, description={self.description}, status={self.status}, dueDate={self.dueDate}, createdAt={self.createdAt}, updatedAt={self.updatedAt})>'


class Tag(Base):
    """
    Define the Tag table as a child of the Base class - It is an ORM Model
    Class maps to the 'tags' table in the database
    """

    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    tasks: Mapped[List['Task']] = relationship(
        'Task', secondary='task_tags', back_populates='tags'
    ) # defines a relationship with 'Task', for the SQLAlchemy model -> many-to-many relationship
    # 'secondary' task_tags, specifies the association table
    # 'back_populates' tags, tells to create a 'tasks' attribute on the 'Task' model that will contain  a list of tasks associated with the task
    



task_tags = Table(
    'task_tags',
    Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
)


def init_db():
    """
    Uses metadata of the Base class to create all the defined tables in the database connection, engine.
    """
    Base.metadata.create_all(
        bind=engine
    )  # creates all tables defined by classes inherited from Base, which includes Task table.
