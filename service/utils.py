BASE_ALPH = tuple("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
BASE_DICT = dict((c, v) for v, c in enumerate(BASE_ALPH))
BASE_LEN = len(BASE_ALPH)

def base_decode(string):
  num = 0
  for char in string:
    num = num * BASE_LEN + BASE_DICT[char]
  return num

def base_encode(num):
  encoding = ""
  while num:
    num, rem = divmod(num, BASE_LEN)
    # Construct the string in reverse so it's easier to decode.
    encoding = BASE_ALPH[rem] + encoding
  return encoding

