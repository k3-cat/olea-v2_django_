import random


ID_ALPHABET = ('0123456789aAbBcC'
               'dDeEfFgGhHiIjJkK'
               'lLmMnNoOpPqQrRsS'
               'tTuUvVwWxXyYzZ_-')

def generate_id(k):
    return ''.join(random.choices(ID_ALPHABET, k=k))
