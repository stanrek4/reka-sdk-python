# This file was auto-generated by Fern from our API Definition.

import json
import os
import typing
import urllib.parse
from json.decoder import JSONDecodeError

import httpx

from .core.api_error import ApiError
from .core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from .core.jsonable_encoder import jsonable_encoder
from .core.remove_none_from_dict import remove_none_from_dict
from .core.request_options import RequestOptions
from .core.unchecked_base_model import construct_type
from .environment import RekaEnvironment
from .errors.unprocessable_entity_error import UnprocessableEntityError
from .types.chat_response import ChatResponse
from .types.chat_round import ChatRound
from .types.chunk_chat_response import ChunkChatResponse
from .types.http_validation_error import HttpValidationError
from .types.model import Model

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class Reka:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propogate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : RekaEnvironment
        The environment to use for requests from the client. from .environment import RekaEnvironment



        Defaults to RekaEnvironment.DEFAULT



    api_key : typing.Optional[str]
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests by default the timeout is 60 seconds, unless a custom httpx client is used, in which case a default is not set.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.Client]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from reka.client import Reka

    client = Reka(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: RekaEnvironment = RekaEnvironment.DEFAULT,
        api_key: typing.Optional[str] = os.getenv("REKA_API_KEY"),
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.Client] = None,
    ):
        _defaulted_timeout = timeout if timeout is not None else 60 if httpx_client is None else None
        if api_key is None:
            raise ApiError(body="The client must be instantiated be either passing in api_key or setting REKA_API_KEY")
        self._client_wrapper = SyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            api_key=api_key,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.Client(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.Client(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
        )

    def chat_stream(
        self,
        *,
        messages: typing.Sequence[ChatRound],
        model: str,
        frequency_penalty: typing.Optional[float] = OMIT,
        max_tokens: typing.Optional[int] = OMIT,
        presence_penalty: typing.Optional[float] = OMIT,
        seed: typing.Optional[int] = OMIT,
        stop: typing.Optional[typing.Sequence[str]] = OMIT,
        temperature: typing.Optional[float] = OMIT,
        top_k: typing.Optional[int] = OMIT,
        top_p: typing.Optional[float] = OMIT,
        use_search_engine: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Iterator[ChunkChatResponse]:
        """
        Parameters
        ----------
        messages : typing.Sequence[ChatRound]

        model : str

        frequency_penalty : typing.Optional[float]

        max_tokens : typing.Optional[int]

        presence_penalty : typing.Optional[float]

        seed : typing.Optional[int]

        stop : typing.Optional[typing.Sequence[str]]

        temperature : typing.Optional[float]

        top_k : typing.Optional[int]

        top_p : typing.Optional[float]

        use_search_engine : typing.Optional[bool]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Yields
        ------
        typing.Iterator[ChunkChatResponse]


        Examples
        --------
        from reka import ChatRound
        from reka.client import Reka

        client = Reka(
            api_key="YOUR_API_KEY",
        )
        client.chat_stream(
            frequency_penalty=1.1,
            max_tokens=1,
            messages=[
                ChatRound(
                    content="string",
                    role="user",
                )
            ],
            model="string",
            presence_penalty=1.1,
            seed=1,
            stop=["string"],
            temperature=1.1,
            top_k=1,
            top_p=1.1,
            use_search_engine=True,
        )
        """
        _request: typing.Dict[str, typing.Any] = {"messages": messages, "model": model, "stream": True}
        if frequency_penalty is not OMIT:
            _request["frequency_penalty"] = frequency_penalty
        if max_tokens is not OMIT:
            _request["max_tokens"] = max_tokens
        if presence_penalty is not OMIT:
            _request["presence_penalty"] = presence_penalty
        if seed is not OMIT:
            _request["seed"] = seed
        if stop is not OMIT:
            _request["stop"] = stop
        if temperature is not OMIT:
            _request["temperature"] = temperature
        if top_k is not OMIT:
            _request["top_k"] = top_k
        if top_p is not OMIT:
            _request["top_p"] = top_p
        if use_search_engine is not OMIT:
            _request["use_search_engine"] = use_search_engine
        with self._client_wrapper.httpx_client.stream(
            method="POST",
            url=urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "chat"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(_request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(_request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        ) as _response:
            if 200 <= _response.status_code < 300:
                for _text in _response.iter_lines():
                    if len(_text) == 0:
                        continue
                    yield typing.cast(ChunkChatResponse, construct_type(type_=ChunkChatResponse, object_=json.loads(_text)))  # type: ignore
                return
            _response.read()
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(HttpValidationError, construct_type(type_=HttpValidationError, object_=_response.json()))  # type: ignore
                )
            try:
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)

    def chat(
        self,
        *,
        messages: typing.Sequence[ChatRound],
        model: str,
        frequency_penalty: typing.Optional[float] = OMIT,
        max_tokens: typing.Optional[int] = OMIT,
        presence_penalty: typing.Optional[float] = OMIT,
        seed: typing.Optional[int] = OMIT,
        stop: typing.Optional[typing.Sequence[str]] = OMIT,
        temperature: typing.Optional[float] = OMIT,
        top_k: typing.Optional[int] = OMIT,
        top_p: typing.Optional[float] = OMIT,
        use_search_engine: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ChatResponse:
        """
        Parameters
        ----------
        messages : typing.Sequence[ChatRound]

        model : str

        frequency_penalty : typing.Optional[float]

        max_tokens : typing.Optional[int]

        presence_penalty : typing.Optional[float]

        seed : typing.Optional[int]

        stop : typing.Optional[typing.Sequence[str]]

        temperature : typing.Optional[float]

        top_k : typing.Optional[int]

        top_p : typing.Optional[float]

        use_search_engine : typing.Optional[bool]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ChatResponse


        Examples
        --------
        from reka import ChatRound
        from reka.client import Reka

        client = Reka(
            api_key="YOUR_API_KEY",
        )
        client.chat(
            messages=[
                ChatRound(
                    content="content",
                    role="user",
                )
            ],
            model="model",
        )
        """
        _request: typing.Dict[str, typing.Any] = {"messages": messages, "model": model, "stream": False}
        if frequency_penalty is not OMIT:
            _request["frequency_penalty"] = frequency_penalty
        if max_tokens is not OMIT:
            _request["max_tokens"] = max_tokens
        if presence_penalty is not OMIT:
            _request["presence_penalty"] = presence_penalty
        if seed is not OMIT:
            _request["seed"] = seed
        if stop is not OMIT:
            _request["stop"] = stop
        if temperature is not OMIT:
            _request["temperature"] = temperature
        if top_k is not OMIT:
            _request["top_k"] = top_k
        if top_p is not OMIT:
            _request["top_p"] = top_p
        if use_search_engine is not OMIT:
            _request["use_search_engine"] = use_search_engine
        _response = self._client_wrapper.httpx_client.request(
            method="POST",
            url=urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "chat"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(_request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(_request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return typing.cast(ChatResponse, construct_type(type_=ChatResponse, object_=_response.json()))  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(
                typing.cast(HttpValidationError, construct_type(type_=HttpValidationError, object_=_response.json()))  # type: ignore
            )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_models_models_get(self, *, request_options: typing.Optional[RequestOptions] = None) -> typing.List[Model]:
        """
        List models available to the user.

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[Model]
            Successful Response

        Examples
        --------
        from reka.client import Reka

        client = Reka(
            api_key="YOUR_API_KEY",
        )
        client.get_models_models_get()
        """
        _response = self._client_wrapper.httpx_client.request(
            method="GET",
            url=urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "models"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return typing.cast(typing.List[Model], construct_type(type_=typing.List[Model], object_=_response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncReka:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propogate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : RekaEnvironment
        The environment to use for requests from the client. from .environment import RekaEnvironment



        Defaults to RekaEnvironment.DEFAULT



    api_key : typing.Optional[str]
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests by default the timeout is 60 seconds, unless a custom httpx client is used, in which case a default is not set.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.AsyncClient]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from reka.client import AsyncReka

    client = AsyncReka(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: RekaEnvironment = RekaEnvironment.DEFAULT,
        api_key: typing.Optional[str] = os.getenv("REKA_API_KEY"),
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.AsyncClient] = None,
    ):
        _defaulted_timeout = timeout if timeout is not None else 60 if httpx_client is None else None
        if api_key is None:
            raise ApiError(body="The client must be instantiated be either passing in api_key or setting REKA_API_KEY")
        self._client_wrapper = AsyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            api_key=api_key,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
        )

    async def chat_stream(
        self,
        *,
        messages: typing.Sequence[ChatRound],
        model: str,
        frequency_penalty: typing.Optional[float] = OMIT,
        max_tokens: typing.Optional[int] = OMIT,
        presence_penalty: typing.Optional[float] = OMIT,
        seed: typing.Optional[int] = OMIT,
        stop: typing.Optional[typing.Sequence[str]] = OMIT,
        temperature: typing.Optional[float] = OMIT,
        top_k: typing.Optional[int] = OMIT,
        top_p: typing.Optional[float] = OMIT,
        use_search_engine: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.AsyncIterator[ChunkChatResponse]:
        """
        Parameters
        ----------
        messages : typing.Sequence[ChatRound]

        model : str

        frequency_penalty : typing.Optional[float]

        max_tokens : typing.Optional[int]

        presence_penalty : typing.Optional[float]

        seed : typing.Optional[int]

        stop : typing.Optional[typing.Sequence[str]]

        temperature : typing.Optional[float]

        top_k : typing.Optional[int]

        top_p : typing.Optional[float]

        use_search_engine : typing.Optional[bool]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Yields
        ------
        typing.AsyncIterator[ChunkChatResponse]


        Examples
        --------
        from reka import ChatRound
        from reka.client import AsyncReka

        client = AsyncReka(
            api_key="YOUR_API_KEY",
        )
        await client.chat_stream(
            frequency_penalty=1.1,
            max_tokens=1,
            messages=[
                ChatRound(
                    content="string",
                    role="user",
                )
            ],
            model="string",
            presence_penalty=1.1,
            seed=1,
            stop=["string"],
            temperature=1.1,
            top_k=1,
            top_p=1.1,
            use_search_engine=True,
        )
        """
        _request: typing.Dict[str, typing.Any] = {"messages": messages, "model": model, "stream": True}
        if frequency_penalty is not OMIT:
            _request["frequency_penalty"] = frequency_penalty
        if max_tokens is not OMIT:
            _request["max_tokens"] = max_tokens
        if presence_penalty is not OMIT:
            _request["presence_penalty"] = presence_penalty
        if seed is not OMIT:
            _request["seed"] = seed
        if stop is not OMIT:
            _request["stop"] = stop
        if temperature is not OMIT:
            _request["temperature"] = temperature
        if top_k is not OMIT:
            _request["top_k"] = top_k
        if top_p is not OMIT:
            _request["top_p"] = top_p
        if use_search_engine is not OMIT:
            _request["use_search_engine"] = use_search_engine
        async with self._client_wrapper.httpx_client.stream(
            method="POST",
            url=urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "chat"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(_request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(_request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        ) as _response:
            if 200 <= _response.status_code < 300:
                async for _text in _response.aiter_lines():
                    if len(_text) == 0:
                        continue
                    yield typing.cast(ChunkChatResponse, construct_type(type_=ChunkChatResponse, object_=json.loads(_text)))  # type: ignore
                return
            await _response.aread()
            if _response.status_code == 422:
                raise UnprocessableEntityError(
                    typing.cast(HttpValidationError, construct_type(type_=HttpValidationError, object_=_response.json()))  # type: ignore
                )
            try:
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)

    async def chat(
        self,
        *,
        messages: typing.Sequence[ChatRound],
        model: str,
        frequency_penalty: typing.Optional[float] = OMIT,
        max_tokens: typing.Optional[int] = OMIT,
        presence_penalty: typing.Optional[float] = OMIT,
        seed: typing.Optional[int] = OMIT,
        stop: typing.Optional[typing.Sequence[str]] = OMIT,
        temperature: typing.Optional[float] = OMIT,
        top_k: typing.Optional[int] = OMIT,
        top_p: typing.Optional[float] = OMIT,
        use_search_engine: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> ChatResponse:
        """
        Parameters
        ----------
        messages : typing.Sequence[ChatRound]

        model : str

        frequency_penalty : typing.Optional[float]

        max_tokens : typing.Optional[int]

        presence_penalty : typing.Optional[float]

        seed : typing.Optional[int]

        stop : typing.Optional[typing.Sequence[str]]

        temperature : typing.Optional[float]

        top_k : typing.Optional[int]

        top_p : typing.Optional[float]

        use_search_engine : typing.Optional[bool]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ChatResponse


        Examples
        --------
        from reka import ChatRound
        from reka.client import AsyncReka

        client = AsyncReka(
            api_key="YOUR_API_KEY",
        )
        await client.chat(
            messages=[
                ChatRound(
                    content="content",
                    role="user",
                )
            ],
            model="model",
        )
        """
        _request: typing.Dict[str, typing.Any] = {"messages": messages, "model": model, "stream": False}
        if frequency_penalty is not OMIT:
            _request["frequency_penalty"] = frequency_penalty
        if max_tokens is not OMIT:
            _request["max_tokens"] = max_tokens
        if presence_penalty is not OMIT:
            _request["presence_penalty"] = presence_penalty
        if seed is not OMIT:
            _request["seed"] = seed
        if stop is not OMIT:
            _request["stop"] = stop
        if temperature is not OMIT:
            _request["temperature"] = temperature
        if top_k is not OMIT:
            _request["top_k"] = top_k
        if top_p is not OMIT:
            _request["top_p"] = top_p
        if use_search_engine is not OMIT:
            _request["use_search_engine"] = use_search_engine
        _response = await self._client_wrapper.httpx_client.request(
            method="POST",
            url=urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "chat"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            json=jsonable_encoder(_request)
            if request_options is None or request_options.get("additional_body_parameters") is None
            else {
                **jsonable_encoder(_request),
                **(jsonable_encoder(remove_none_from_dict(request_options.get("additional_body_parameters", {})))),
            },
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return typing.cast(ChatResponse, construct_type(type_=ChatResponse, object_=_response.json()))  # type: ignore
        if _response.status_code == 422:
            raise UnprocessableEntityError(
                typing.cast(HttpValidationError, construct_type(type_=HttpValidationError, object_=_response.json()))  # type: ignore
            )
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def get_models_models_get(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.List[Model]:
        """
        List models available to the user.

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[Model]
            Successful Response

        Examples
        --------
        from reka.client import AsyncReka

        client = AsyncReka(
            api_key="YOUR_API_KEY",
        )
        await client.get_models_models_get()
        """
        _response = await self._client_wrapper.httpx_client.request(
            method="GET",
            url=urllib.parse.urljoin(f"{self._client_wrapper.get_base_url()}/", "models"),
            params=jsonable_encoder(
                request_options.get("additional_query_parameters") if request_options is not None else None
            ),
            headers=jsonable_encoder(
                remove_none_from_dict(
                    {
                        **self._client_wrapper.get_headers(),
                        **(request_options.get("additional_headers", {}) if request_options is not None else {}),
                    }
                )
            ),
            timeout=request_options.get("timeout_in_seconds")
            if request_options is not None and request_options.get("timeout_in_seconds") is not None
            else self._client_wrapper.get_timeout(),
            retries=0,
            max_retries=request_options.get("max_retries") if request_options is not None else 0,  # type: ignore
        )
        if 200 <= _response.status_code < 300:
            return typing.cast(typing.List[Model], construct_type(type_=typing.List[Model], object_=_response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


def _get_base_url(*, base_url: typing.Optional[str] = None, environment: RekaEnvironment) -> str:
    if base_url is not None:
        return base_url
    elif environment is not None:
        return environment.value
    else:
        raise Exception("Please pass in either base_url or environment to construct the client")
