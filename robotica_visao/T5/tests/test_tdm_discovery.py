from tdmclient import ClientAsync


with ClientAsync() as client:

    async def main():
        print("A procurar Thymio através do TDM...", flush=True)

        node = await client.wait_for_node()

        print("Thymio encontrado!", flush=True)
        print("ID:", node.id, flush=True)

    client.run_async_program(main)
