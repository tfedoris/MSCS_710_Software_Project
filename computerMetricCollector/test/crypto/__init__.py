
def read_key(keyFile):
    with open(keyFile) as f:
        key = f.read()
    return key