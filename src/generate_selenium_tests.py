
import asyncio
from workflow import run_workflow

if __name__ == "__main__":
    async def main():
        target_url = "https://www.google.com/"
        query = "Test searching for the term 'Rachel' and verify that results appear."

        result = await run_workflow(query, target_url)
       # print("Final State:", result)

    asyncio.run(main())
