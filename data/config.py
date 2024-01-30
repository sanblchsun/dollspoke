from environs import Env


# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
PAYMENTS_TOKEN = env.str("PAYMENTS_TOKEN")
# ADMINS = list(map(str.strip, env.list("ADMINS")))  # Тут у нас будет список из админов
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

