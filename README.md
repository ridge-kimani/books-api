**Library API**

#### Setup

```bash
# create virtual-env
$ python3 -m venv venv

# activate
$ source venv_name/bin/activate

# install dependencies
$ pip install -r requirements.txt

# create .env
$ touch .env 

# Copy values from .env-sample 
cat .env-sample >> .env # Replace the values with the correct ones

# update migrations
$ alembic upgrade head

# Run server
$ python server.py

# Seed data
$ curl -X POST http://localhost:5000/seed
```
