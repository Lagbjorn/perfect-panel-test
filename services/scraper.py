import aiohttp

from config import DESKTOP_HEADERS, MOBILE_HEADERS


class BaseVKScraper:
    vk_url = 'https://vk.com/'
    m_vk_url = 'https://m.vk.com/'

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()


class VKScraper(BaseVKScraper):
    async def scrape_profile(self, username, mobile) -> str:
        url = (self.m_vk_url if mobile else self.vk_url) + username
        params = {'act': 'info'} if mobile else None
        return await self._scrape(url, mobile=mobile, params=params)

    async def scrape_profile_posts(self, username, num) -> str:
        url = self.m_vk_url + username
        params = {'offset': num}
        return await self._scrape(url, mobile=True, params=params)

    async def scrape_post(self, post_url) -> str:
        return await self._scrape(post_url, mobile=True)

    async def _scrape(self, url, mobile: bool = True, params=None) -> str:
        cookies = {'remixlang': 3}  # ensure we parse english version

        async with self.session.get(
            url,
            cookies=cookies,
            params=params,
            headers=MOBILE_HEADERS if mobile else DESKTOP_HEADERS,
        ) as response:
            return await response.text()


async def get_scraper():
    async with VKScraper() as scraper:
        yield scraper
