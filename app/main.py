import asyncio
from app.tasks.fetch_and_process import _run_async_pipeline

if __name__ == "__main__":
    print("Starting host data pipeline...")
    asyncio.run(_run_async_pipeline())
    print("Pipeline completed successfully.")