import re

from bs4 import BeautifulSoup

from api.v1.schemas.response.data import PostData, ProfileData


class VKProfileParser:
    profile_page: BeautifulSoup
    profile_url_prefix = 'https://vk.com/id'

    def __init__(self, profile_html, m_profile_html):
        self.profile_page = BeautifulSoup(profile_html, 'html.parser')
        self.m_profile_page = BeautifulSoup(m_profile_html, 'html.parser')

    def get_profile_info(self):
        return ProfileData(
            followers=self._get_followers_count(),
            following=self._get_following_count(),
            avatar_url=self._get_avatar_url(),
            profile_id=self._get_profile_id(),
        )

    def _get_following_count(self) -> int:
        following_label = self.m_profile_page.find(
            'div',
            class_='Menu__itemTitle',
            string=re.compile('Following'),
        )
        count = following_label.find_next_sibling(class_='Menu__itemCount')
        if count:
            return int(count.string)
        else:
            raise AttributeError('Following counter is not found in HTML document')

    def _get_followers_count(self) -> int:
        followers_div = self.m_profile_page.find(
            'div',
            class_='OwnerInfo__rowCenter',
            string=re.compile('followers'),
        )
        count = ''.join((d for d in followers_div.string if d.isdigit()))
        return int(count)

    def _get_avatar_url(self) -> str:
        return self.profile_page.find(class_='page_avatar_img')['src']

    def _get_profile_id(self) -> str:
        profile_url = self.profile_page.find(property='og:url')['content']
        if profile_url.startswith(self.profile_url_prefix):
            return profile_url[len(self.profile_url_prefix):]


class VKPostParser:
    page: BeautifulSoup

    def __init__(self, page):
        self.page = BeautifulSoup(page, 'html.parser')

    def get_single_post_stats(self):
        url = self._get_canonical_url()
        return PostData(
            likes=self._get_likes(),
            share=self._get_share(),
            views=self._get_views(),
            post_id=self._id_from_url(url),
            url=url,
        )

    def _get_likes(self) -> str:
        try:
            return self.page.find(class_='v_like').string
        except AttributeError as e:
            if self.page.find(class_='item_like'):
                return '0'
            else:
                raise e

    def _get_share(self) -> str:
        try:
            return self.page.find(class_='v_share').string
        except AttributeError as e:
            if self.page.find(class_='item_share'):
                return '0'
            else:
                raise e

    def _get_views(self) -> str:
        views_string = self.page.find(class_='Socials__button_views')['aria-label']
        return ''.join((d for d in views_string if d.isdigit()))

    def _get_canonical_url(self) -> str:
        return self.page.find('link', rel='canonical')['href']

    @staticmethod
    def _id_from_url(url) -> str:
        prefix = 'https://vk.com/wall'
        if url.startswith(prefix):
            return url[len(prefix):]
        else:
            raise ValueError('Canonical url should be formatted as "https://vk.com/wall<post_id>"')
