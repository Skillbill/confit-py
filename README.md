# Python Confit Client

python3 client to load configurations from confit

## Install

```
$ python3 setup.py install --prefix=${prefix}
```

## Usage

```
from confit import client
import json

repo_id = 'wOgys75iJVWmuL4Ykx1dBHgSsp03'
secret = 'f801cf39-b784-414e-b997-231b9cc51ebe'
c = client.Client(repo_id, secret)
try:
	data = c.load('/prod/config.json')
	cfg = json.loads(data)
except ValueError as err:
       print(f'could not load configuration: {err}')
```
