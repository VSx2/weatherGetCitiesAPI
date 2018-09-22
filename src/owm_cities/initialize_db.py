import sys
import json
import redis
import argparse
import configparser


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
        for i in value:
            r = redis.StrictRedis(
                host=local_conf.get('redis.host') or 'localhost',
                port=local_conf.get('redis.port') or 6379,
                db=local_conf.get('redis.db') or 0
            )
            if i.get('name'):
                val = {}
                for j in i.keys():
                    val[j] = i[j]
                r.sadd(i.get('name').lower(), json.dumps(val))
