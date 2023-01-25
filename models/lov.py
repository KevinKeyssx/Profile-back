# SqlAchemy
from sqlalchemy         import Column, Integer, String, ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm     import relationship
from sqlalchemy_json    import MutableJson

# Roles and Permissions
from database import Base
from datetime import datetime


class Lov( Base ):
    __tablename__ = 'list_of_values'

    id              = Column(Integer,       primary_key = True, index       = True)
    description     = Column(String( 100 ), unique      = True, nullable    = False)
    active          = Column(Boolean,       default     = True, nullable    = False)
    skill           = Column(MutableJson,   default     = '{}')
    created_at      = Column(DateTime,      default     = datetime.now(), nullable = False)
    comment         = Column( Text )


class Lov_Vals( Base ):
    __tablename__ = 'lov_vals'

    id              = Column(Integer,       primary_key = True, index = True)
    lov_id          = Column(Integer,       ForeignKey('list_of_values.id'))
    description     = Column(String( 100 ), unique  = True, nullable = False)
    active          = Column(Boolean,       default = True, nullable = False)
    skill           = Column(MutableJson,   default = '{}')
    created_at      = Column(DateTime,      default = datetime.now(), nullable = False)
    comment         = Column( Text )
    # Relacion con LOV
    lov             = relationship(Lov, lazy = 'joined')