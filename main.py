from http.cookiejar import debug

from app.app import init_app

app = init_app()

if __name__ == '__main__':
    app.run_server(debug=True)