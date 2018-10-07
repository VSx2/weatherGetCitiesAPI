
import sys
import tornado.web
import tornado.gen
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

import argparse
import configparser

from tornado_sqlalchemy import (
    make_session_factory,
    SessionMixin
)
from .models import City

ALLOWED_FIELDS = set(["name", "id", "country", "coord"])


class ApiHandler(SessionMixin, tornado.web.RequestHandler):

    # modes:
    # 0 - search by first letter(-s)
    # 1 - search by "ilike"
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
            q = self.get_argument('q', '').lower()
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
        query = '{}%'.format(q)
        if mode == '1':
            query = '%' + query
        elif mode != '0':
            self.set_status(404)
            result_dict['errors'].append("Invalid mode")
            return self.finish(result_dict)
        with self.make_session() as session:
            # Unable to do async
            # (SQLite objects created in a thread can
            # only be used in that same thread.)
            select_attrs = []
            for i in fields:
                select_attrs.append(getattr(City, i))
            items = session.query(*select_attrs).filter(City.name.like(query))\
                .order_by(City.id)
            total_items = items.count()
            if limit:
                try:
                    limit = int(limit)
                except ValueError:
                    self.set_status(400)
                    result_dict['errors'].append("Invalid limit")
                    return self.finish(result_dict)
                items = items.limit(limit)
            if offset:
                try:
                    offset = int(offset or 0)
                except ValueError:
                    self.set_status(400)
                    result_dict['errors'].append("Invalid offset")
                    return self.finish(result_dict)
                items = items.offset(offset)

            result = []

            for j in items:
                tmp_result = {}
                for field in fields:
                    tmp_result[field] = getattr(j, field)
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
    def __init__(self, config):
        tornado.ioloop.IOLoop.configure(
            'tornado.platform.asyncio.AsyncIOMainLoop'
        )

        handlers = [
            (r"/", MainHandler),
            (r"/api", ApiHandler),
            (r"/doc", DocHandler)
        ]
        session_factory = make_session_factory(
            config.get('db_connection') or 'sqlite:///cities.db'
        )

        super().__init__(handlers, session_factory=session_factory, debug=True)


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

    application = Application(local_conf)
    http_server = HTTPServer(application)
    http_server.listen(local_conf.get('web.port') or 8888)
    IOLoop.current().start()


if __name__ == '__main__':
    main()
