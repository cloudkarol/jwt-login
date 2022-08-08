import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:

    __name__: str

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
    id = sa.Column(
        psql.UUID(as_uuid=True),
        server_default=sa.text('uuid_generate_v4()'),
        primary_key=True,
        index=True,
    )