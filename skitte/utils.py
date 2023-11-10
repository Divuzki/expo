import string
import random



def truncate_string(value, max_length=45, suffix="skt"):
    string_value = str(value)
    string_truncated = string_value[:min(
        len(string_value), (max_length - len(suffix)))]
    suffix = (suffix if len(string_value) > max_length else '')
    return suffix+string_truncated


def random_string_generator(size=50, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
