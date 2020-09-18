from pathlib import Path
import importlib.util
import os

api_module = None


def import_api(script_filename):
    global api_module
    # if api_module is already loaded, there is nothing to do
    if api_module:
        return

    script_path = Path(script_filename)
    os.chdir(script_path.parent.parent)
    api_module_filepath = 'api.py'
    api_module_name = 'api'
    spec = importlib.util.spec_from_file_location(api_module_name, api_module_filepath)
    api_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(api_module)


def parse_request(environ):
    if 'CONTENT_LENGTH' in environ:
        try:
            post_length = int(environ['CONTENT_LENGTH'])
            req_corpo = environ['wsgi.input'].read(post_length).decode('utf-8')
        except ValueError:
            req_corpo = None
    else:
        req_corpo = None

    req_path = environ.get('PATH_INFO', '')
    req_query = environ.get('QUERY_STRING', '')

    if len(req_path) > 0 and req_path[0] == '/':
        func_name = req_path[1:]
    else:
        func_name = 'errore'

    return {
        'req_corpo': req_corpo,
        'func_name': func_name,
        'req_query': req_query
    }


def application(environ, start_response):
    status = '200 OK'
    response_headers = []
    output = b''

    import_api(environ['SCRIPT_FILENAME'])
    request_parts = parse_request(environ)
    try:
        response = getattr(api_module, request_parts['func_name'])(
            corpo=request_parts['req_corpo'],
            query=request_parts['req_query']
        )
        if len(response) == 0:
            response_headers.append(('Content-type', 'text/plain'))
            output = b'Errore! Risposta vuota!'
        elif response[0] == '<':
            response_headers.append(('Content-type', 'text/html'))
            output = bytes(response, encoding='utf-8')
        elif response[0] in '{[':
            response_headers.append(('Content-type', 'application/json'))
            output = bytes(response, encoding='utf-8')
    except AttributeError:
        response_headers.append(('Content-type', 'text/plain'))
        output = b'Errore! Path non implementato!'

    response_headers.append(('Content-Length', str(len(output))))

    start_response(status, response_headers)
    yield output
