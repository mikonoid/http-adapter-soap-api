#!/usr/bin/python3
import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from urllib3.util.ssl_ import create_urllib3_context
from zeep import Client, Transport
 
BASE_URL = 'https://url_to_api_wsdl'
URL = '{}/index.asmx?WSDL'.format(BASE_URL)
 
USERNAME = 'user'
PASSWORD = 'PASSWORD WAS STOLEN BY UFO'
 
CIPHERS = (
    'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
    'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES:!aNULL:'
    '!eNULL:!MD5'
)
 
 
class DESAdapter(HTTPAdapter):
    """
    A TransportAdapter that re-enables 3DES support in Requests.
    """
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).init_poolmanager(*args, **kwargs)
 
    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).proxy_manager_for(*args, **kwargs)
 
session = requests.Session()
session.mount(BASE_URL, DESAdapter())
session.auth = HTTPBasicAuth(USERNAME, PASSWORD)
#response = session.get(URL, auth=HTTPBasicAuth(USERNAME, PASSWORD))
#print(response.text)
 
client = Client(wsdl=URL, transport=Transport(session=session))
result = client.service.GetCustomerStatus(domainName='cleancore.co.uk')
 
print(result)
