# coding:utf-8


from .home import create_app

app = create_app('develop')


@app.route('/index')
def index():
    return 'index page'


if __name__ == '__main__':
    app.run()
