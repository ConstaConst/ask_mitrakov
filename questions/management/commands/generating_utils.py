import string
import random


def generate_word(word_len=10, chars=string.ascii_letters):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(word_len))


def generate_text(words=10, word_len=10, chars=string.ascii_letters):
    return ' '.join(generate_word(word_len, chars) for _ in range(words))
