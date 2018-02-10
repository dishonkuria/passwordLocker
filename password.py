from hashlib import sha256

def get_hexdigest(salt, plaintext):
    return sha256(salt + plaintext).hexdigest()

SECRET_KEY = 's3cr3t'

def make_password(plaintext, service):
    salt = get_hexdigest(SECRET_KEY, service)[:20]
    hsh = get_hexdigest(salt, plaintext)
    return ''.join((salt, hsh))

ALPHABET = ('abcdefghijklmnopqrstuvwxyz'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            '0123456789!@#$%^&*()-_')

def password(plaintext, service, length=10):
    raw_hexdigest = make_password(plaintext, service)

    # Convert the hexdigest into decimal
    num = int(raw_hexdigest, 16)

    # What base will we convert `num` into?
    num_chars = len(ALPHABET)

    # Build up the new password one "digit" at a time,
    # up to a certain length
    chars = []
    while len(chars) < length:
        num, idx = divmod(num, num_chars)
        chars.append(ALPHABET[idx])

    return ''.join(chars)

from peewee import *

db = SqliteDatabase('accounts.db')

class Service(Model):
    name = CharField()
    length = IntegerField(default=8)
    symbols = BooleanField(default=True)
    alphabet = CharField(default='')

    class Meta:
        database = db

    def get_alphabet(self):
        if self.alphabet:
            return self.alphabet
        alpha = ('abcdefghijklmnopqrstuvwxyz'
                 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                 '0123456789')
        if self.symbols:
            alpha += '!@#$%^&*()-_'
        return alpha

    def password(self, plaintext):
        return password(plaintext, self.name, self.length)

    @classmethod
    def search(cls, q):
        return cls.select().where(cls.name ** ('%%%s%%' % q))

db.create_table(Service, True)
