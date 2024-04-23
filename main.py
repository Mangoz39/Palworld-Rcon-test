import asyncio

class RconClient:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.reader = None
        self.writer = None

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        if self.writer:
            print("Connected!")

    async def disconnect(self):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()

    async def send_command(self, command):
        message = self.build_rcon_message(command)
        self.writer.write(message)
        await self.writer.drain()

    async def receive_response(self):
        response = await self.reader.read(4096)
        return response.decode('utf-8')

    def build_rcon_message(self, command):
        return f"{len(command) + 10}\x00\x00\x00\x00rcon{command}\x00".encode('utf-8')


async def main():
    # RCON 伺服器的連接資訊
    rcon_host = "192.168.50.200"
    rcon_port = 25575  # RCON 伺服器的連接埠
    rcon_password = "catfat"

    rcon_client = RconClient(rcon_host, rcon_port, rcon_password)
    await rcon_client.connect()

    # 發送 RCON 指令
    await rcon_client.send_command("/broadcast hi")

    # 接收伺服器的回應
    response = await rcon_client.receive_response()
    print(response)

    # 斷開 RCON 連線
    await rcon_client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
