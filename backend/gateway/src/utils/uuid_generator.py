import uuid

class UUIDGenerator:
    @classmethod
    def uuid_v4(cls):
        return uuid.uuid4().hex
