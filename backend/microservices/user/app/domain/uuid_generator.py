import uuid

class UUIDGenerator:
    @staticmethod
    def generate():
        return uuid.uuid4().hex
