import os

from src import create_app

env_name = os.environ['FLASK_ENV']

app = create_app(env_name)

if __name__ == '__main__':

    if env_name == 'development':
        from livereload import Server
        server = Server(app.wsgi_app)
        server.serve()
    app.run()

