from fastmcp import Client
import asyncio

async def main():
    async with Client("http://localhost:8070/mcp/", auth="oauth") as client:
        print("✓ Authenticated with Auth0!")

        result = await client.call_tool("fetch_workouts")
        print(f"✅ Successfully fetched workouts!")
        print(f"📊 Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())