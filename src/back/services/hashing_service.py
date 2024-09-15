import bcrypt


class HashingService:

    @staticmethod
    def encrypt(pwd: str) -> str:
        hashed_password = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('ascii')

    @staticmethod
    def verify(provided_pwd: str, hashed_pwd: str) -> bool:
        return bcrypt.checkpw(provided_pwd.encode("utf-8"), hashed_pwd.encode("ascii"))
