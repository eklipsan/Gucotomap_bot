import subprocess
import asyncio
from bot import main


async def run_bot():
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
    await main()

asyncio.run(run_bot())
