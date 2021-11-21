from pydantic import BaseModel


class BaseProfileData(BaseModel):
    profile_id: str
    avatar_url: str


class ProfileData(BaseProfileData):
    followers: str
    following: str


class PostData(BaseModel):
    post_id: str
    url: str
    likes: str
    share: str
    views: str


class ProfilePostsData(BaseProfileData):
    posts: list[PostData]
