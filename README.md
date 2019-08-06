# Making A Server

## What is a server?
In most projects, a server is needed to handle requests, heavy computation, interact with databases, etc. 

## What is this project?
The most simple backend route you can think of. A single endpoint that returns a json blob.

## What is an endpoint?
When you visit a website, the various paths you can traverse are referred to as endpoints.\

## How do I run this?

### Locally
pip install requirements.txt
python app.py

That's it!

### Hosted
heroku login

heroku create my-simple-server

git add .
git commit -m "my simple server"
git push heroku master
