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
    'sqlite:///./tasks.db'  # , echo=True
)  # connect to the database, and enable logging of all the statements

sessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # factory for database sessions (managing connections) -> ensure transactions are not automatically comitted



 # Define an association table for the many-to-many relationship between tasks and tags
task_tags = Table(
    'task_tags',
    Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
)


# Define an association table for the self-referential many-to-many relationship between tasks
task_links = Table(
    'task_links',
    Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id'), primary_key=True),
    Column('linked_task_id', Integer, ForeignKey('tasks.id'), primary_key=True)
) # stores pairs (task_1_id, task_2_id) so these two are linked



class Task(Base):
    """
    Define the Task class as a child of the Base class - It is an ORM Model
    Class maps to the 'tasks' table in the database
    """

    __tablename__ = 'tasks' 

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(nullable=False) 
    # field, title, which is a string and required
    description: Mapped[Optional[str]] = mapped_column(nullable=True) 
    # field, description, which is a string
    status: Mapped[Optional[str]] = mapped_column(default='to-do') 
    # field, status, which is a string and default as 'to-do'
    dueDate: Mapped[Optional[dt.datetime]] = mapped_column(nullable=True)
    # field, dueDate, which is a datetime object
    createdAt: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now) 
    # field, createdAt, which is a DateTime object and default as current time
    updatedAt: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now, onupdate=dt.datetime.now) 
    # field, updatedAt, which is a DateTime object and defaults and updates as current time
    
    # Parent-child relationship logic 
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey('tasks.id'), nullable=True)  
    # field, parent_id, which is an integer and a foreign key to the 'tasks' table itself (adjaency list)
    # creates a column that will point to another row in the same table, if null it is a top-level task.
    parent: Mapped[Optional['Task']] = relationship('Task', remote_side=[id], back_populates='subtasks') 
    # task.parent -> get the parent task of a subtask
    # remote_id -> look at the ID field to find the parent.
    subtasks: Mapped[List['Task']] = relationship('Task', back_populates='parent')  # task.subtasks -> get list of subtasks for a parent task


    # Tag relationship logic - many-to-many relationship
    tags: Mapped[List['Tag']] = relationship('Tag', secondary='task_tags', back_populates='tasks') 
    # task.tags -> get list of tags associated with a task
    # 'secondary'=task_tags: specifies the association table and tells SQLAlchemy where to look for these connections

    # Linked tasks relationship logic - self-referential many-to-many relationship
    links: Mapped[List['Task']] = relationship(
        'Task',
        secondary='task_links', # use that association table
        primaryjoin=id == task_links.c.task_id, # Task.id links to task_links.task_id
        secondaryjoin=id == task_links.c.linked_task_id, # Task.id links to task_links.linked_task_id
        back_populates='_links_reverse'
    )  # task.links -> get list of tasks linked to this task
    _links_reverse: Mapped[List['Task']] = relationship(
        'Task',
        secondary='task_links',  # use that association table
        primaryjoin=id == task_links.c.linked_task_id, # Task.id links to task_links.linked_task_id
        secondaryjoin=id == task_links.c.task_id, # Task.id links to task_links.task_id
        back_populates='links'
    )  # task._links_reverse -> get list of tasks that link to this task
    


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
    )  # defines a relationship with 'Task', for the SQLAlchemy model -> many-to-many relationship
    # 'secondary' task_tags, specifies the association table
    # 'back_populates' tags, tells to create a 'tasks' attribute on the 'Task' model that will contain  a list of tasks associated with the task
    
    def __repr__(self):
        """
        Defines how an instance of the Tag class should be represented as a string, for logging
        """
        return f'<Tag(id={self.id}, name={self.name})>'
    

def init_db():
    """
    Uses metadata of the Base class to create all the defined tables in the database connection, engine.
    """
    Base.metadata.create_all(
        bind=engine
    )  # creates all tables defined by classes inherited from Base, which includes Task table.
