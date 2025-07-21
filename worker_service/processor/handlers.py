import asyncio

async def process_echo(payload: str) -> str:
    return payload

async def process_reverse(payload: str) -> str:
    return payload[::-1]

async def process_cpu_intensive(payload: str) -> str:
    await asyncio.sleep(10)
    return "done"
