import os
from flask_script import Manager
from api import create_app
import unittest

app = create_app(config_name='development')
manager = Manager(app)


@manager.command
def  run():
        app.run()

@manager.command
def test():

        tests = unittest.TestLoader().discover('tests', pattern='test*.py')
        result = unittest.TextTestRunner(verbosity=2).run(tests)

        if result.wasSuccessful():
                return 0

        return 1

if __name__ == '__main__':
        manager.run()
