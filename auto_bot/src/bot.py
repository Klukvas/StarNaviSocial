from src.service import Service
from src.utils.logger import setup_custom_logger
from typing import Optional
import random
import threading
class Bot:
    
    def __init__(
            self, 
            service: Service, 
            max_interactions_per_user:int,
            max_posts_per_user:int,
            max_retries: Optional[int] = 2
        ) -> None:
        self.service = service
        self.token = None
        self.max_interactions_per_user = max_interactions_per_user
        self.max_posts_per_user = max_posts_per_user
        self.max_retries = max_retries
        self.total_likes = 0
        self.total_dislikes = 0
    
    def _register_customer(self):
        response = self.service.register_new_customer()
        if response:
            json = response.json()
            self.token = json['access_token']['token']
            self.logger.info('Customer registered')
        else:
            raise ValueError(f"Retry limit reached for customer registration.\nError: {response}")

    def _create_post(self):
        response = self.service.create_post(token=self.token)
        if response:
            self.logger.info('Post created')
            return response.json()
        if not response:
            raise ValueError(f"Retry limit reached for post creation.\nError: {response}")
    
    def _like_post(self, post_id: int):
        response = self.service.like_post(post_id=post_id, token=self.token)
        if response:
            self.logger.info(f'Post {post_id} liked')
            self.total_likes += 1
        else:
            raise ValueError(f"Retry limit reached for post like.\nError: {response}")

    def _dislike_post(self, post_id: int):
        response = self.service.dislike_post(post_id=post_id, token=self.token)
        if response:
            self.logger.info(f'Post {post_id} disliked')
            self.total_dislikes += 1
        else:
            raise ValueError(f"Retry limit reached for post dislike.\nError: {response}")


    def start_emulate_user(self) -> None:
        self.logger = setup_custom_logger(threading.current_thread().name)
        self.logger.info(f'Start to emulate user activity')
        self._register_customer()
        self.logger.debug(f'User registered')
        self.post_ids = [
            self._create_post()['id']
            for _ in range(self.max_posts_per_user)
        ]
        for _ in range(self.max_interactions_per_user):
            fn = random.choice([self._like_post, self._dislike_post])
            post_id = random.choice(self.post_ids)
            fn(post_id)
        self.logger.info(f'Work done.\nStats: total_dislikes: {self.total_dislikes}\ntotal_likes: {self.total_likes}')


        
            



