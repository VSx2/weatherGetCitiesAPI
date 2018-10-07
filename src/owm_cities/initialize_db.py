import sys
import json

import argparse
import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from .models import DeclarativeBase, City


def main(argv=sys.argv):
    description = """\
        Initialize cities on selected Redis DB
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        'config_uri',
        metavar='config_uri',
        help='Path to configuration file'
    )
    parser.add_argument(
        'file_uri',
        metavar='file_uri',
        help='Path to source json file uri(can be downloaded on owm.com)'
    )

    args = parser.parse_args(argv[1:])
    config_uri = args.config_uri
    config = configparser.ConfigParser()
    config.read(config_uri)
    local_conf = config['DEFAULT']

    with open(args.file_uri, 'rb') as file:
        try:
            value = json.loads(file.read())
        except Exception as e:
            print(e)
            sys.exit()
        Session = sessionmaker()
        engine = create_engine(
            local_conf.get('db_connection') or 'sqlite:///cities.db'
        )
        Session.configure(bind=engine)

        DBSession = Session()

        DeclarativeBase.metadata.create_all(engine)
        for i in value:
            if i.get('name'):
                city = City()
                city.map_data(i)
                try:
                    DBSession.add(city)
                    DBSession.flush()
                except SQLAlchemyError as e:
                    print('DB Error')
                    raise e
        DBSession.commit()
