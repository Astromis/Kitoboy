import sys
import json
import traceback
from functools import wraps
from sqlalchemy.exc import ProgrammingError


class DbException(Exception):
    pass


def get_traceback_msg(*args):
    """Returns traceback's error message until 2nd level"""
    er_type, _, tb = sys.exc_info()
    tb_ifo = traceback.extract_tb(tb, limit=2)
    return f'{tb_ifo[1:]} {er_type}  ' + ' '.join([str(i) for i in args])


def error_handler(logger):
    """Decorator for handling and logging errors"""

    def wrapper_1(func):
        @wraps(func)
        def wrapper_2(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except json.JSONDecodeError:
                logger.error(get_traceback_msg())
                return {'error': 'Request\'s body is empty'}, 502

            except ProgrammingError as exp:
                logger.error(get_traceback_msg(exp))
                return {'error': 'An error occurred '
                                 'while processing request'}, 502

            except DbException as exp:
                logger.error(get_traceback_msg(exp))
                return {'error': 'An error occurred '
                                 'while processing request'}, 502

            except AttributeError as exp:
                logger.error(get_traceback_msg(exp))
                return {'error': 'Wrong arguments were passed'}, 404

            except TypeError as exp:
                logger.error(get_traceback_msg(exp))
                return {'error': 'Wrong params were passed'}, 502

            except ValueError as exp:
                logger.error(get_traceback_msg(exp))
                return {'error': 'Wrong params were passed'}, 404

            except KeyError as exp:
                logger.error(get_traceback_msg(exp))
                return {'error': 'Wrong arguments were passed'}, 404

            except Exception as exp:
                logger.error(get_traceback_msg(exp))
                return {'error': 'An error occurred '
                                 'while processing request'}, 502

        return wrapper_2

    return wrapper_1
