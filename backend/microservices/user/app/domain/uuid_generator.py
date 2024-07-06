import uuid

class UUIDGenerator:
    @staticmethod
    def generate():
        return str(uuid.uuid4().hex())
