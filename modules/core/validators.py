import re


def check_password_format(value):
    if value is not None and not is_empty(value) and contain_minimal_size(value, 8) and contain_numbers(value) and contain_alpha(value):
        return True
    else:
        return False


def is_empty(value):
    if len(value) == 0:
        return True
    else:
        return False


def contain_minimal_size(value,size):
    return check_pattern(r'\w{'+str(size)+',}', value)


def contain_numbers(value):
    return check_pattern(r'\d', value)


def contain_alpha(value):
    return check_pattern(r'[a-zA-Z]', value)


def check_pattern(pattern,value):
    if re.search(pattern, value):
        return True
    else:
        return False
