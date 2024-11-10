from db.base import Base

from sqlalchemy.dialects.postgresql import UUID
import uuid

from sqlalchemy import Column, Numeric, String
from sqlalchemy.types import JSON

class Counsel(Base):
    __tablename__ = 'counsels'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # counsel for day # in original order (somewhat chronological)
    original_order = Column('original_order', Numeric)
    # counsel for day # in random order
    random_order = Column('random_order', Numeric)
    # counsel body
    counsel = Column('counsel', String(1500)) # initial max is 1109
    # counsel reference
    reference = Column('reference', String(100)) # initial max is 80
    
    # optional JSON field for possible extentions and adaptions
    optional = Column('optional', JSON)

    def __init__(self, original_order, random_order, counsel, reference, optional=None):
        self.original_order = original_order
        self.random_order = random_order
        self.counsel = counsel
        self.reference = reference
        self.optional = optional