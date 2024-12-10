#import __init__.py from market folder

from market import app

if __name__ == '__main__':
    app.run(debug=True)