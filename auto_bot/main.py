
from src.utils import read_config
from concurrent.futures import ThreadPoolExecutor
from src.bot import Bot
from src.service import Service

def start(config: dict):
    service: Service = Service(
        port=config['service_settings']['port'],
        host=config['service_settings']['host']
    )
    with ThreadPoolExecutor() as executor:
        executor.map(
            lambda _: Bot(
                service=service,
                max_posts_per_user=config['bot_settings']['max_posts_per_user'],
                max_interactions_per_user=config['bot_settings']['max_interactions_per_user']
            ).start_emulate_user(),
            range(config['bot_settings']['number_of_users'])
        )

def test(config: dict):
    service: Service = Service(
        port=config['service_settings']['port'],
        host=config['service_settings']['host']
    )
    Bot(
        service=service,max_posts_per_user=config['bot_settings']['max_posts_per_user'],
        max_interactions_per_user=config['bot_settings']['max_interactions_per_user']
    ).start_emulate_user()
    
if __name__ == '__main__':
    config = read_config()
    start(config)