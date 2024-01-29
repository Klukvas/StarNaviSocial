from sqlalchemy.ext.asyncio import AsyncSession

from src.models import PostInteractionsModel, PostModel, UserModel
from src.schemas import MessageResponse
from src.schemas.post_schema import PostBase, PostDb
from src.utils.exception import ExceptionError


class PostController:

    @staticmethod
    async def create_new_post(post: PostBase, session: AsyncSession, user: UserModel):
        created_post = await PostModel.create(
            post=post, author_id=user.id, session=session
        )
        return PostDb.from_orm(created_post).model_dump()
    @staticmethod
    async def like_post(
        post_id: int, 
        user: UserModel, 
        session: AsyncSession
    ):
        post = await PostModel.find_by_id(post_id, session)
        if post:
            prev_interacton = await PostInteractionsModel.getUserInteractionsByPost(
                user_id=user.id, post_id=post.id, session=session
            )
            if prev_interacton:
                if prev_interacton.is_like:  # means user wanna remove like
                    await PostInteractionsModel.deleteIneraction(
                        interaction_id=prev_interacton.id, session=session
                    )
                    await PostModel.decrease_likes(post_id=post.id, session=session)
                    return MessageResponse(message="Post unliked successfully")
                else:  # change from dislike to like
                    await PostInteractionsModel.updateState(
                        interaction_id=prev_interacton.id, new_state=True, session=session
                    )
                    await PostModel.switch_count_interactions(
                        post_id=post.id, incrementToLikes=True, session=session
                    )
                    return MessageResponse(message="Post liked successfully")
            else:
                await PostInteractionsModel.insertNewInteraction(
                    user_id=user.id, post_id=post.id, state=True, session=session
                )
                await PostModel.increase_likes(post_id=post.id, session=session)
                return MessageResponse(message="Post liked successfully")
        else:
            raise ExceptionError(status_code=404, message="Post not found")

    @staticmethod
    async def dislike_post(
        post_id: int,
        user: UserModel,
        session: AsyncSession
    ):
        # find the post
        post = await PostModel.find_by_id(post_id, session)
        if post:
            # find previous interaction with post
            prev_interacton = await PostInteractionsModel.getUserInteractionsByPost(
                user_id=user.id, post_id=post.id, session=session
            )
            if prev_interacton:
                # if previous interaction is like -> change it to dislike
                if prev_interacton.is_like:
                    await PostInteractionsModel.updateState(
                        interaction_id=prev_interacton.id, new_state=False, session=session
                    )
                    await PostModel.switch_count_interactions(
                        post_id=post.id, incrementToLikes=False, session=session
                    )
                    return MessageResponse(message="Post disliked successfully")
                # if previous interaction is dislike -> remove it
                else:
                    await PostInteractionsModel.deleteIneraction(
                        interaction_id=prev_interacton.id, session=session
                    )
                    await PostModel.decrease_dislikes(post_id=post.id, session=session)
                    return MessageResponse(message="Post undisliked successfully")
            else:
                # if previous interaction is not found -> just add new dislike record
                await PostInteractionsModel.insertNewInteraction(
                    user_id=user.id, post_id=post.id, state=False, session=session
                )
                await PostModel.increase_dislikes(post_id=post.id, session=session)
                return MessageResponse(message="Post disliked successfully")
        else:
            raise ExceptionError(status_code=404, message="Post not found")
