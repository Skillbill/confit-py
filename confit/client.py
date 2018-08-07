from os import getenv
from http.client import HTTPConnection, HTTPSConnection

_hostname = getenv('CONFIT_HOST', 'confit.skillbill.net')
_port = getenv('CONFIT_PORT', '443')
_http_connection = HTTPSConnection if getenv('CONFIT_INSECURE', False) == False else HTTPConnection

class Client:
	def __init__(self, repo_id, secret):
		self.repo_id = repo_id
		self.secret = secret

	def _build_url(self, resource, is_alias, ref):
		kind = '/alias/' if is_alias else '/path'
		params = f'?ref={ref}' if ref else ''
		return f'/api/repo/{self.repo_id}/{kind}/{resource}{params}'

	def load(self, resource, is_alias =False, ref=None):
		c = _http_connection(_hostname, _port)
		c.request('GET', self._build_url(resource, is_alias, ref), headers={'Authorization': f'secret {self.secret}'})
		res = c.getresponse()
		data = res.read()
		c.close()
		if res.status != 200:
			raise ValueError(res.reason)
		return data

if __name__ == '__main__':
	import argparse
	import sys

	p = argparse.ArgumentParser()
	p.add_argument('-r', dest='ref', help='ref')
	p.add_argument('-s', dest='secret', help='repo secret')
	p.add_argument('-a', dest='is_alias', action='store_const', const=True, help='resource is alias')
	p.add_argument('repo_id')
	p.add_argument('resource')
	args = p.parse_args(sys.argv[1:])
	c = Client(args.repo_id, args.secret)
	try:
		data = c.load(args.resource, args.is_alias, args.ref)
		print(data.decode('utf-8'))
	except ValueError as err:
		print(err)
		sys.exit(1)
