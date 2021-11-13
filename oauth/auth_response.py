class AuthResponse(dict):
    
    def __init__(self, token: bytes, expiresin: int) -> None:
        self.token = token.decode('utf-8')
        self.expiresin = expiresin
