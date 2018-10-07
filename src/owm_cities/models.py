import json

from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import class_mapper
from tornado_sqlalchemy import declarative_base

DeclarativeBase = declarative_base()


class City(DeclarativeBase):
    __tablename__ = "city"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(1000))
    country = Column(String(1000))
    coord = Column(String(1000), info={'format': 'json'})

    def map_data(self, data):
        for col in class_mapper(self.__class__).mapped_table.c:
            value = data.get(col.name)
            if col.info and col.info.get('format') == 'json':
                try:
                    value = json.dumps(value)
                except (TypeError, ValueError) as e:
                    print('Error mapping entity.')
                    raise e
            setattr(self, col.name, value)
