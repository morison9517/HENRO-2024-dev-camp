from decouple import config

try:
    secret = config('LINE_CHANNEL_SECRET')
    print(f'LINE_CHANNEL_SECRET: {secret}')
except Exception as e:
    print(f'Error: {e}')