import hashlib

def sha256_hash(text):
    # Encode the text to bytes, then hash it
    hashed = hashlib.sha256(text.encode('utf-8')).hexdigest()
    return hashed