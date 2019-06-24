# -*- coding: utf-8 -*- 
import datetime
import fcntl
import os
import re
import urllib.parse
# try:
#     from urllib.parse import urlparse
# except ImportError:
#      from urlparse import urlparse

from HTTP_request import HTTP_request
from constants import MIME_TYPES,\
						 RESPONSE_CODES,\
						  RESPONSE_OK,\
						   RESPONSE_FAIL,\
						    DATETIME_TEMPLATE,\
						     ALLOW_METHODS

def build_response(resp_code = '', 
					protocol = '', 
					content_type  = '', 
					content_length = '') :
	if resp_code == RESPONSE_CODES["OK"]:
		return RESPONSE_OK.format(protocol,
									resp_code,
									content_type,
									content_length,
									datetime.datetime.utcnow().strftime(DATETIME_TEMPLATE)).encode()
	else:
		return RESPONSE_FAIL.format(protocol, 
									resp_code).encode()


def parse_request(request_string):
	request = HTTP_request()
	try:
		request.method = re.findall(r'^(\w+)', request_string)[0]
	except IndexError:
		request.method = None
	try:
		request.protocol = re.findall(r'HTTP/([0-9.]+)', request_string)[0]
		# request.protocol = "1.1"
	except IndexError:
		request.protocol = None
	try:
		request.url = re.findall(r'([^\s?]+)', request_string)[1]
		request.url = urllib.parse.unquote(request.url)
	except IndexError:
		request.url = None
	# request.query = re.findall(r'[?&]([\w=]+)', rr)
	# request.query = {item.split("=")[0]: item.split("=")[1] for item in 
	# 	re.findall(r'[?&]([\w=]+)', rr)}
	# request.headers
	return request

def request_processing(request_string, document_root = ''):
	'''Обработка запроса, формирование ответа'''

	request = parse_request(request_string) 	

	protocol = request.protocol
	response = None
	file_path = None

	# Не тот метод
	if request.method not in ALLOW_METHODS:
		return build_response(RESPONSE_CODES["NOT_ALLOWED"], protocol), None

	# Много поднимаемся наверх по папкам
	if len(re.findall(r'\.\./', request.url)) > 1:
		return build_response(RESPONSE_CODES["FORBIDDEN"], protocol), None

	request.url += 'index.html' if request.url[-1] == '/' else ''
	file_path = request.url[1:]

	try:
		file = os.open(os.path.join(document_root, file_path), os.O_RDONLY)
		flag = fcntl.fcntl(file, fcntl.F_GETFL)
		fcntl.fcntl(file, fcntl.F_SETFL, flag | os.O_NONBLOCK)
	except (FileNotFoundError, IsADirectoryError):
		if 'index.html' in  request.url:
			return build_response(RESPONSE_CODES["FORBIDDEN"], protocol), None
		else:
			return build_response(RESPONSE_CODES["NOT_FOUND"], protocol), None 
	except OSError:
		return build_response(RESPONSE_CODES["NOT_FOUND"], protocol), None 

	try:
		content_type = MIME_TYPES[re.findall(r'\.(\w+)$', file_path)[0]]
	except KeyError:
		content_type = MIME_TYPES["default"]

	content_length = os.path.getsize(os.path.join(document_root, file_path))

	if request.method == 'HEAD':
		file = None

	return build_response(RESPONSE_CODES["OK"], protocol, content_type, content_length), file
