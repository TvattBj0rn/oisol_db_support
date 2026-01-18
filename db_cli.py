import logging
import sys

from src.operations import TypeColumns

if __name__ == '__main__':
    if len(sys.argv) != 2:
        logging.warning('> At least one parameter must be provided')
        exit()
    db_path = sys.argv[1]

    operation_type = input('What operation should be done ?\n - 1. Typing\n - 2. New column\n> ')

    if operation_type.lower() in ['1', 'typing']:
        TypeColumns(db_path)
    elif operation_type.lower() in ['2' 'new column', 'new']:
        pass
    else:
        logging.warning('The operation you wrote does not exists')
