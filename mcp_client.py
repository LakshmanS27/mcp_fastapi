import asyncio
# from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient
from os import getenv
from dotenv import load_dotenv

load_dotenv()

async def main():
    config = {
        "mcpServers": {
            "my_fastapi_mcp": {
                "url": "http://localhost:8081/mcp"
            }
        }
    }



    llm = ChatOpenAI(
        api_key=getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        model="nvidia/nemotron-3-nano-30b-a3b:free",
    )

    client = MCPClient.from_dict(config)
    # llm = ChatOllama(model="llama3.2:1b")
    agent = MCPAgent(llm=llm, client=client, max_steps=30)

    print("MCP Agent Chat (type 'exit' to quit)\n")

    while True:
        query = input("You: ")
        if query.lower() in ("exit", "quit"):
            break

        result = await agent.run(query)
        print(f"Agent: {result}\n")

    await client.close_all_sessions()

asyncio.run(main())
