from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime as dt

Base = (
    declarative_base()
)  # Any class that inheirts from Base is considered a SQLAlchemy ORM model


class Task(Base):
    """
    Class maps to the task table in the database
    """

    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)  # primary key field, id, which is an integer
    description = Column(
        String, nullable=False
    )  # ield, description, which is a string and required
    status = Column(
        String, default='to-do'
    )  # field, status, which is a string and default as 'to-do'
    createdAt = Column(
        DateTime, default=dt.datetime.now
    )  # field, createdAt, which is a DateTime object and default as current time
    updatedAt = Column(
        DateTime, default=dt.datetime.now, onupdate=dt.datetime.now
    )  # field, updatedAt, which is a DateTime object and defaults and updates as current time

    def __repr__(self):
        """
        Defines how an instance of the Task class should be represented as a string
        """
        return f'Task(id={self.id}, description={self.description}, status={self.status}, createdAt={self.createdAt}, updatedAt={self.updatedAt})'


engine = create_engine(
    'sqlite:///./tasks.db', echo=True
)  # connect to the database, and log all the statements

sessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # factory for database sessions (managing connections)


def init_db():
    """
    Uses metadata of the Base class to create all the defined tables in the database connection, engine.
    """
    Base.metadata.create_all(bind=engine)
