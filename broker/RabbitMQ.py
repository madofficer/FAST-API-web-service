import aio_pika
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool

class RabbitMQService:
    def __init__(self, connection_string: str):
        self.connection_pool = Pool(
            lambda: aio_pika.connect_robust(connection_string),
            max_size=2
        )

    async def get_connection(self) -> AbstractRobustConnection:
        return await self.connection_pool.acquire()

    async def publish_task(self, task_uuid: str):
        connection = await self.get_connection()
        async with connection:
            channel = await connection.channel()
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=task_uuid.encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key="task_queue"
            )