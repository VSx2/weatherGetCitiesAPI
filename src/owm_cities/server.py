
import sys
import tornado.web
import tornado.gen

import aioredis
import asyncio

import json
import argparse
import configparser

ALLOWED_FIELDS = set(["name", "id", "country", "coord"])


class ApiHandler(tornado.web.RequestHandler):

    # modes:
    # 0 - search by first letter(-s)
    # 1 - search by "ilike"
    @asyncio.coroutine
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        result_dict = {
            'errors': [],
            'items': [],
            'status': 'error',
        }

        mode = self.get_argument('mode', None)
        try:
            q = self.get_argument('q', None).lower()
            fields = self.get_argument('fields', 'name,id').split(',')
        except SyntaxError:
            self.set_status(400)
            result_dict['errors'].append("Invalid Query or Fields")
            return self.finish(result_dict)
        for i in fields:
            if i not in ALLOWED_FIELDS:
                result_dict['errors'].append("Invalid field: {}".format(i))
        if result_dict['errors']:
            self.set_status(400)
            return self.finish(result_dict)
        limit = self.get_argument('limit', None)
        offset = self.get_argument('offset', None)
        self.set_header("Content-Type", "application/json")

        if not q:
            self.set_status(400)
            result_dict['errors'].append("Empty Query")
            return self.finish(result_dict)
        query = '{}*'.format(q)
        if mode == '1':
            query = '*' + query
        elif mode != '0':
            self.set_status(404)
            result_dict['errors'].append("Invalid mode")
            return self.finish(result_dict)
        redis = self.application.redis
        try:
            db_keys = yield from redis.keys(query)  # NOQA
        except aioredis.errors.ReplyError:
            result_dict['errors'] = 'Error loading data from DB.'
            self.set_status(500)
            return self.finish(result_dict)
        result = []
        if limit:
            try:
                limit = int(limit)
            except ValueError:
                self.set_status(400)
                result_dict['errors'].append("Invalid limit")
                return self.finish(result_dict)
            try:
                offset = int(offset or 0)
            except ValueError:
                self.set_status(400)
                result_dict['errors'].append("Invalid offset")
                return self.finish(result_dict)

            total_items = len(db_keys)
            db_keys = db_keys[offset * limit:(offset + 1) * limit]
        for i in db_keys:
            val = yield from redis.smembers(i)
            for j in val:
                tmp_val = json.loads(j)
                tmp_result = {}
                for field in fields:
                    tmp_result[field] = tmp_val[field]
                result.append(tmp_result)
        result_dict['items'] = result
        result_dict['total_items'] = total_items
        result_dict['status'] = 'success'
        self.finish(result_dict)


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("templates/index.html")


class DocHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("templates/doc.html")


class Application(tornado.web.Application):
    def __init__(self):
        tornado.ioloop.IOLoop.configure(
            'tornado.platform.asyncio.AsyncIOMainLoop'
        )

        handlers = [
            (r"/", MainHandler),
            (r"/api", ApiHandler),
            (r"/doc", DocHandler)
        ]

        super().__init__(handlers, debug=True)

    def init_with_loop(self, loop, config):
        redis_db = 0
        try:
            redis_db = int(config.get('redis.db'))
        except ValueError:
            print("redis.db must be integer. Use default value(0)")
        self.redis = loop.run_until_complete(
            aioredis.create_redis(
                (
                    config.get('redis.host') or 'localhost',
                    config.get('redis.port') or 6379
                ),
                db=int(config.get('redis.db')) or 0,
                loop=loop
            )
        )


def main(argv=sys.argv):
    description = """
        Start server and api
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        'config_uri',
        metavar='config_uri',
        help='Path to configuration file'
    )
    args = parser.parse_args(argv[1:])
    config_uri = args.config_uri
    config = configparser.ConfigParser()
    config.read(config_uri)
    local_conf = config['DEFAULT']

    application = Application()
    application.listen(local_conf.get('web.port') or 8888)

    loop = asyncio.get_event_loop()
    application.init_with_loop(loop, local_conf)
    loop.run_forever()


if __name__ == '__main__':
    main()
