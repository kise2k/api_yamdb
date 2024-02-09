NAME_CONST_CHAR = 256
SLUG_CONST_CHAR = 50
LENGTH_FOR_ADMIN = 25
MIN_CONST_SCORE_VALUE = 1
MAX_CONST_SCORE_VALUE = 10
FIELD_LEN_150 = 150
FIELD_LEN_254 = 254
MIN_COSNT_FOR_YEAR = 0

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'
ROLES = (
    (USER, 'Пользователь'),
    (ADMIN, 'Администратор'),
    (MODERATOR, 'Модератор')
)

REGEX_PATTERN = r'^[\w.@+-]+\Z'
REGEX_ALLOWS = 'a-z/A-Z/0-9/. /@ /+/- '
