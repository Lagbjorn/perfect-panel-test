from enum import Enum

from pydantic import AnyHttpUrl, BaseModel, validator


class Method(str, Enum):
    PROFILE = 'profile'
    LIKES = 'likes'
    POSTS = 'posts'


class ProfileQuery(BaseModel):
    profile: str

    @validator('profile')
    def vk_id_validation(cls, name):
        """Validation rules from https://vk.com/faq18038"""
        if not 5 <= len(name) <= 32:
            raise ValueError('ID length must be between 5 and 32')
        if name[0] == '_' or name[-1] == '_':
            raise ValueError('"_" is not allowed both at start and end of the string')
        if all(d in '1234567890' for d in name[:3]):
            raise ValueError('3 or more consecutive digits are not allowed at start')
        return name


class LikesQuery(BaseModel):
    link: AnyHttpUrl

    @validator('link')
    def host_validation(cls, url):
        if not (url.startswith('https://vk.com/wall') or url.startswith('https://m.vk.com/wall')):
            raise ValueError('Scraper only connects to vk.com or m.vk.com')
        return url


class PostsQuery(ProfileQuery):
    pass


METHOD_PARAMS = {
    Method.PROFILE: ProfileQuery,
    Method.LIKES: LikesQuery,
    Method.POSTS: PostsQuery,
}
