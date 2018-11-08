import re
import traceback

from bookdb import BookDB

DB = BookDB()


def book(book_id):
    book = DB.title_info(book_id)
    try:
        book_info = ['<h1>{}</h1>'.format(book['title']), '<table>']
        book_info.append('<tr><th>Author</th><td>{}</td></tr>'.format(book['author']))
        book_info.append('<tr><th>Publisher</th><td>{}</td></tr>'.format(book['publisher']))
        book_info.append('<tr><th>ISBN</th><td>{}</td></tr>'.format(book['isbn']))
    except TypeError:
        raise NameError

    return '\n'.join(book_info)


def books():
    book_list = ['<h1>Here is a list of books!</h1>\n', '<ul>']

    for book in DB.titles():
        book_list.append('<li><a href="/book/{}">{}</a></li>'.format(book['id'],
                                                                     book['title']))
    book_list.append('</ul>')

    return '\n'.join(book_list)


def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


def resolve_path(path):
    funcs = {'': books,
             'book': book}

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
