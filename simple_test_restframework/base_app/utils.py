from hashids import Hashids

hasher = Hashids(salt='TeSt-ReSt_FrAmEwOrK', min_length=8)

def encode_id(id):
    """Encrypt an ID."""
    return hasher.encode(id)

def decode_id(hashid):
    """Decrypt a hashid."""
    decoded = hasher.decode(hashid)
    return decoded[0] if decoded else None