from db.base import Base, Session

from sqlalchemy.dialects.postgresql import UUID
import uuid

from sqlalchemy import Column, String, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from utils.utils import get_epoch, shift_12h_tf

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    subscriber_id = Column(Numeric, ForeignKey('subscribers.id'))
    # selected devotional name
    devotional_name = Column('devotional_name', String(128))
    
    # subscriber-defined preffered time to receive devotionals
    preferred_time_local = Column('preferred_time_local', String(10))
    # system-translated preffered time to send devotionals
    preferred_time_utc = Column('preferred_time_utc', String(10))
    # utc offset respect bot's location
    utc_offset = Column('utc_offset', Integer)
    # subscription creation time in UTC
    creation_utc = Column('creation_utc', Numeric)

    # -700 is PST to UTC offset (in summer)
    def __init__(self, subscriber_id, devotional_name=None, preferred_time_local='10pm', utc_offset=-700, creation_utc=get_epoch()):
        self.subscriber_id = subscriber_id
        self.devotional_name = devotional_name
        self.preferred_time_local = preferred_time_local
        self.utc_offset = utc_offset
        self.preferred_time_utc = shift_12h_tf(preferred_time, utc_offset)
        self.creation_utc = creation_utc

    def update_utc_offset(self, offset):
        self.utc_offset = offset
        self.preferred_time_utc = shift_12h_tf(self.preferred_time_local, self.utc_offset)

    def update_preferred_time_local(self, new_time):
        self.preferred_time_local = new_time
        self.preferred_time_utc = shift_12h_tf(self.preferred_time_local, self.utc_offset)

    def persist(self):
        session = Session()
        session.add(self)
        session.commit()
        session.close()

    def delete(self):
        session = Session()
        session.delete(self)
        session.commit()
        session.close()