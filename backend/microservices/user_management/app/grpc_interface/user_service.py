from grpc_interface import user_service_pb2_grpc
from application.user_handler import UserHandler

class UserServiceServicer(user_service_pb2_grpc.UserServiceServicer):
    def __init__(self, user_handler: UserHandler):
        self.user_handler = user_handler

    async def Register(self, request, context):
        return await self.user_handler.Register(request, context)

    async def AuthenticatePhoneNumber(self, request, context):
        return await self.user_handler.AuthenticatePhoneNumber(request, context)

    async def Login(self, request, context):
        return await self.user_handler.Login(request, context)

    async def GetUserInfo(self, request, context):
        return await self.user_handler.GetUserInfo(request, context)

    async def AddAddress(self, request, context):
        return await self.user_handler.AddAddress(request, context)

    async def ModifyAddress(self, request, context):
        return await self.user_handler.ModifyAddress(request, context)

    async def DeleteAddress(self, request, context):
        return await self.user_handler.DeleteAddress(request, context)

    async def SetPreferredAddress(self, request, context):
        return await self.user_handler.SetPreferredAddress(request, context)
