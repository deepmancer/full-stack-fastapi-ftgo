from  rabbitmq_rpc import RPCClient, RabbitMQConfig
import asyncio

async def main():
    rab = RabbitMQConfig(
        host='rabbitmq',
        user='rabbitmq_user',
        password='rabbitmq_password',
        ssl_connection=False,
        port=5672,
    )

    cl = await RPCClient.create(config=rab)
    data = {
        "first_name": "Alireza",
        "last_name": "Heidari",
        "phone_number": "09435364283",
        "password": "1#FDFKqaz2wsx",
        "role": "driver",
        "national_id": "242342"
    }
    result = await cl.call('user.profile.create', data)
    print(result)
    
asyncio.run(main())