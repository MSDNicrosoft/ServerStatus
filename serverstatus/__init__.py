from mcdreforged.api.all import *
from mcstatus import MinecraftServer as Connect
from time import sleep
from typing import Dict


class ServerConfig(Serializable):
    name: str = "Server"
    host: str = "localhost"
    port: int = 25565


class Config(Serializable):
    servers: Dict[str, ServerConfig] = {
        'Survival': ServerConfig(port=25565),
        'Mirror': ServerConfig(port=25566),
        'Creative': ServerConfig(port=25567)
    }


config: Config
CONFIG_FILE = "config/ServerStatus/config.json"


def on_load(server: PluginServerInterface):
    global config
    config = server.load_config_simple(CONFIG_FILE, target_class=Config, in_data_folder=False)



def on_server_startup(server: PluginServerInterface):
    info = config.servers.items()
    _ = len(info) - 1
    a = 0
    while True:
        if not a == _:
            Ping(server, Name=info[a]['name'], Host=info[a]['host'], Post=info[a]['port'])
            a += 1


@new_thread
def Ping(server, Name="Server", Host="127.0.0.1", Port=25585):
    i = Connect(host=Host, port=Port)
    status = True
    while True:
        sleep(5)
        del _
        try:
            _ = i.status()
        except (ConnectionResetError, ConnectionRefusedError):
            if status:
                server.say(f"§6{Name} §c关啦！")
                status = False
        if not status:
            server.say(f"§6{Name} §2开啦！")
