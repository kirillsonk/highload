MIME_TYPES = {
	'html': 'text/html',
	'css': 'text/css',
	'js': 'text/javascript',
	'jpg': 'image/jpeg',
	'jpeg': 'image/jpeg',
	'png': 'image/png',
	'gif': 'image/gif',
	'swf': 'application/x-shockwave-flash',
	'txt': 'text/txt',
	'default': 'text/plain'
}

RESPONSE_CODES = {
	'OK': '200 OK',
	'NOT_FOUND': '404 Not Found',
	'NOT_ALLOWED': '405 Method Not Allowed',
	'FORBIDDEN': '403 Forbidden'
}

RESPONSE_OK = 'HTTP/{} {}\r\n' \
			'Content-Type: {}\r\n' \
			'Content-Length: {}\r\n'\
			'Date: {}\r\n' \
			'Server: PythonServer\r\n\r\n'

RESPONSE_FAIL = 'HTTP/{} {}\r\n' \
			'Server: PythonServer'

DATETIME_TEMPLATE = '%a, %d %b %Y %H:%M:%S GMT'

ALLOW_METHODS = ['HEAD', 'GET']