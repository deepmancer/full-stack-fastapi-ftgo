import asyncio
from rabbitmq_rpc import RPCClient


async def main():
    data  = {
        "first_name": "Alireza",
        "last_name": "Heidari",
        "phone_number": "09435264283",
        "password": "1#FDFKqaz2wsx",
        "role": "customer",
        "national_id": "242342"
    }
    rpc_client = await RPCClient.create(
        host='localhost',
        port=5920,
        user='rabbitmq_user',
        password='rabbitmq_password',
        vhost='/',
        ssl=False,
    )
    
    result = await rpc_client.call('user.profile.create', data=data)
    print(result)
    
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())