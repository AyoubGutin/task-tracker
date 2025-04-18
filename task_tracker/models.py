from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
)  # modules for db operations
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import (
    sessionmaker,
)  # object-relational mapper (ORM) - bridge between OOP amd relational dbs
import datetime as dt


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

    id = Column(Integer, primary_key=True)  # primary key field, id, which is an integer

    title = Column(
        String, nullable=False
    )  # field, title, which is a string and required
    description = Column(String, nullable=True)  # field, description, which is a string
    status = Column(
        String, default='to-do'
    )  # field, status, which is a string and default as 'to-do'
    dueDate = Column(DateTime, nullable=True)
    createdAt = Column(
        DateTime, default=dt.datetime.now
    )  # field, createdAt, which is a DateTime object and default as current time
    updatedAt = Column(
        DateTime, default=dt.datetime.now, onupdate=dt.datetime.now
    )  # field, updatedAt, which is a DateTime object and defaults and updates as current time

    def __repr__(self):
        """
        Defines how an instance of the Task class should be represented as a string, for logging
        """
        return f'<Task(id={self.id}, title={self.title}, description={self.description}, status={self.status}, dueDate={self.dueDate}, createdAt={self.createdAt}, updatedAt={self.updatedAt})>'


def init_db():
    """
    Uses metadata of the Base class to create all the defined tables in the database connection, engine.
    """
    Base.metadata.create_all(
        bind=engine
    )  # creates all tables defined by classes inherited from Base, which includes Task table.
