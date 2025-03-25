import asyncio
import aio_pika
import docker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from concurrent.futures import ThreadPoolExecutor

from source.repository.main import async_engine
from source.tasks.models import Task

docker_client = docker.from_env()
docker_executor = ThreadPoolExecutor(max_workers=4)


async def process_docker_task(task_code: str) -> dict:
    loop = asyncio.get_event_loop()
    try:
        # Запускаем синхронный Docker код в отдельном потоке
        result = await loop.run_in_executor(
            docker_executor,
            lambda: docker_client.containers.run(
                "python:alpine",
                command=f"python -c '{task_code}'",
                detach=True,
                mem_limit='100m',
                cpu_quota=50000,
                network_mode='none',
                remove=True
            )
        )
        return {"status": "completed", "result": result.logs().decode('utf-8')}
    except Exception as e:
        return {"status": "failed", "result": str(e)}


async def update_task(session: AsyncSession, task_uuid: str, status: str, result: str):
    task = await session.get(Task, task_uuid)
    if task:
        task.status = status
        task.result = result
        await session.commit()


async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        task_uuid = message.body.decode()

        Session = sessionmaker(
            bind=async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

        async with Session() as session:
            task = await session.get(Task, task_uuid)
            if not task:
                return

            await update_task(session, task_uuid, "running", None)

            execution_result = await process_docker_task(task.code)

            await update_task(
                session,
                task_uuid,
                execution_result["status"],
                execution_result["result"]
            )


async def main():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()
    queue = await channel.declare_queue("task_queue", durable=True)

    await queue.consume(on_message)

    print("Consumer started. Waiting for messages...")
    try:
        await asyncio.Future()  # Бесконечное ожидание
    finally:
        await connection.close()


if __name__ == "__main__":
    asyncio.run(main())