# Making A Server

## What is this?

This is the most simple backend I can think of. Endpoint '/' returns hello world, and /first_endpoint returns another plain string value.

## What is a server?

In most projects, a server is needed to handle requests, heavy computation, interact with databases, etc.

## What is an endpoint?

When you visit a website, the various paths you can traverse are referred to as endpoints.

## How do I run this?

### Locally

```
pip install requirements.txt
python app.py
```

Open [localhost:5000/first_endpoint](http://localhost:5000/first_endpoint')

That's it!

### Hosted

--> This means people can access it from the internet!

First time:

```
heroku login
heroku create my-app-simple-server
```

Any new changes:

```
git add .
git commit -m "my first server"
git push heroku master
```

Open the url that is generated for you! This will not change between deploys.
