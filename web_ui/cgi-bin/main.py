#!/usr/bin/env python3
import sys
import os
import cgitb
import importlib.util

cgitb.enable()
# cgitb.enable(display=0, logdir="logs/")
# print("Content-Type: text/plain\n")
# print(os.getcwd())
# sys.exit(0)

api_module_name = 'api'
api_module_filepath = 'api.py'
spec = importlib.util.spec_from_file_location(api_module_name, api_module_filepath)
api_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api_module)


if 'CONTENT_LENGTH' in os.environ:
    try:
        post_length = int(os.environ['CONTENT_LENGTH'])
        # post_length stores byte count, but stdin.read, apparently, takes the character count
        req_corpo = sys.stdin.buffer.read(post_length).decode('utf-8')
    except ValueError:
        req_corpo = None
else:
    req_corpo = None

req_path = os.environ.get('PATH_INFO', '')
req_query = os.environ.get('QUERY_STRING', '')

if len(req_path) > 0 and req_path[0] == '/':
    func_name = req_path[1:]
else:
    func_name = 'errore'


try:
    response = getattr(api_module, func_name)(corpo=req_corpo, query=req_query)
    if len(response) == 0:
        print("Content-Type: text/plain\n")
        print('Errore! Risposta vuota!')
    elif response[0] == '<':
        print("Content-Type: text/html\n")
    elif response[0] in '{[':
        print("Content-Type: application/json\n")
    print(response)
except AttributeError:
    print("Content-Type: text/plain\n")
    print('Errore! Path non implementato!')
