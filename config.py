from environs import Env

env = Env()
env.read_env(".env")

PORT = env("PORT")
HOSTNAME = env("HOSTNAME")
PROTOCOL = env("PROTOCOL")
CHARS = env("CHARS")
