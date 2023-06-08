# Python GraphQL server, built with Falcon and Graphene

To install dependencies:
```
python3 -m venv venv
source venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

You need to have PostgreSQL installed, with the following parameters:
```
POSTGRES_PASSWORD=postgres
POSTGRES_USER=postgres
POSTGRES_DB=music_info
```

To run:
```
make start-app
```

To check if it's running, simply:

```
curl http://127.0.01:80/healthcheck
```


To call the GraphQL endpoints, use Postman. Check the collection inside the `postman` folder.


To exit the virtual env, run `deactivate`.