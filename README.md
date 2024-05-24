# Reka Python Library

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-SDK%20generated%20by%20Fern-brightgreen)](https://github.com/fern-api/fern)

The Reka Python Library provides convenient access to the Reka API from
applications written in Python.

The library includes type definitions for all
request and response fields, and offers both synchronous and asynchronous clients powered by httpx.

## Installation

Add this dependency to your project's build file:

```bash
pip install reka-api
# or
poetry add reka-api
```

## Usage

Simply import `Reka` and start making calls to our API.

```python
from reka import ChatRound
from reka.client import Reka

client = Reka(
    api_key="YOUR_API_KEY",
)

client.chat.create(
    messages=[
        ChatRound(
            content="What is the fifth prime number?",
            role="user",
        )
    ],
    model="reka-core-20240501",
)
```

or for multimodality you can do

```python
client.chat.create_stream(
    messages=[
        ChatRound(
            role="user",
            content=[
                {
                    "type": "text",
                    "text": "What is this video about?"
                },
                {
                    "type": "video_url":
                    "video_url": "https://fun_video"
                }
            ],
        )
    ],
    model="reka-core-20240501",
)
```

## Async Client

The SDK also exports an async client so that you can make non-blocking
calls to our API.

```python
import asyncio
from reka import ChatRound
from reka.client import AsyncReka

client = AsyncReka(
    api_key="YOUR_API_KEY",
)

async def main() -> None:
    await client.chat(
        messages=[
            ChatRound(
                content="What is the fifth prime number?",
                role="user",
            )
        ],
        model="reka-core-20240501",
    )
asyncio.run(main())
```

## Streaming

The SDK supports streaming endpoints. To take advantage of this feature for chat,
use `chat_stream`.

```Python
from reka import ChatRound
from reka.client import Reka

client = Reka(
    api_key="YOUR_API_KEY",
)

stream = client.chat_stream(
    messages=[
        ChatRound(
            content="Tell me a short story",
            role="user",
        )
    ],
    model="reka-core-20240501",
)

for message in stream:
    print(message.responses[0].round.content, end='\n---\n')
```

## Exception Handling

All errors thrown by the SDK will be subclasses of [`ApiError`](./src/schematic/core/api_error.py).

```python
import reka

try:
    client.chat(...)
except reka.core.ApiError as e: # Handle all errors
  print(e.status_code)
  print(e.body)
```

## Advanced

### Timeouts

By default, requests time out after 60 seconds. You can configure this with a
timeout option at the client or request level.

```python
from reka.client import Reka

client = Reka(
    ...,
    # All timeouts are 20 seconds
    timeout=20.0,
)

# Override timeout for a specific method
client.chat(..., {
    timeout_in_seconds=20.0
})
```

### Retries

The SDK is instrumented with automatic retries with exponential backoff. A request will be
retried as long as the request is deemed retriable and the number of retry attempts has not grown larger
than the configured retry limit (default: 2).

A request is deemed retriable when any of the following HTTP status codes is returned:

- [408](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/408) (Timeout)
- [429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) (Too Many Requests)
- [5XX](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500) (Internal Server Errors)

Use the `max_retries` request option to configure this behavior.

```python
client.chat(..., {
     max_retries=1
})
```

### Custom HTTP client

You can override the httpx client to customize it for your use-case. Some common use-cases
include support for proxies and transports.

```python
import httpx

from reka.client import Reka

client = Reka(...,
    http_client=httpx.Client(
        proxies="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

## Beta Status

This SDK is in **Preview**, and there may be breaking changes between versions without a major
version update.

To ensure a reproducible environment (and minimize risk of breaking changes), we recommend pinning a specific package version.

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically.
Additions made directly to this library would have to be moved over to our generation code,
otherwise they would be overwritten upon the next generated release. Feel free to open a PR as
a proof of concept, but know that we will not be able to merge it as-is. We suggest opening
an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
