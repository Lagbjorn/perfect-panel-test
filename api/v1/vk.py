from typing import Union

import aiohttp
from fastapi import APIRouter, HTTPException, Request, Depends
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from services.parser import VKPostParser, VKProfileParser
from services.scraper import VKScraper, get_scraper
from .schemas.request import METHOD_PARAMS, Method
from .schemas.response.response import ErrorResponse, Response, Status

router = APIRouter()


@router.get("", response_model=Union[Response, ErrorResponse])
async def get(
    method: Method,
    request: Request,
    scraper: VKScraper = Depends(get_scraper),
):
    # validate input
    try:
        query = METHOD_PARAMS[method](**request.query_params)
    except ValueError:
        return ErrorResponse(
            status=Status.ERROR,
            code=HTTP_400_BAD_REQUEST,
            message='Invalid query params',
        )

    if method == Method.PROFILE:
        try:
            page = await scraper.scrape_profile(query.profile, mobile=False)  # desktop version always contains id
            page_m = await scraper.scrape_profile(query.profile, mobile=True)  # mobile version always contains precise number of followings
        except aiohttp.ClientError:
            return ErrorResponse(
                status=Status.ERROR,
                code=HTTP_403_FORBIDDEN,
                message='No connection with vk.com',
            )

        parser = VKProfileParser(page, page_m)
        try:
            data = parser.get_profile_info()
            return Response(
                status=Status.SUCCESS,
                code=HTTP_200_OK,
                data=data,
            )
        except (AttributeError, ValueError, TypeError):
            return ErrorResponse(
                status=Status.ERROR,
                code=HTTP_403_FORBIDDEN,
                message='Invalid account name',
            )

    if method == Method.LIKES:
        try:
            page = await scraper.scrape_post(query.link)
        except aiohttp.ClientError:
            return ErrorResponse(
                status=Status.ERROR,
                code=HTTP_403_FORBIDDEN,
                message='No connection with vk.com',
            )
        parser = VKPostParser(page)
        try:
            data = parser.get_single_post_stats()
            return Response(
                status=Status.SUCCESS,
                code=HTTP_200_OK,
                data=data,
            )
        except (AttributeError, ValueError, TypeError):
            return ErrorResponse(
                status=Status.ERROR,
                code=HTTP_403_FORBIDDEN,
                message='Invalid post',
            )

    if method == Method.POSTS:
        raise HTTPException(status_code=501, detail="Posts not implemented")
