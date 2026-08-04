import time
import httpx


class HTTPClient:
    def __init__(self, timeout: float = 1.0):
        self._client = httpx.AsyncClient(timeout=httpx.Timeout(timeout))

    async def get(self, url: str) -> dict:
        try:

            start = time.perf_counter()
            response = await self._client.get(url)
            elapsed = time.perf_counter() - start
            return {
                'url': url,
                'elapsed': elapsed,
                'status_code': response.status_code,
                'is_success': 200 <= response.status_code < 400
            }

        except httpx.TimeoutException:
            return {'url': url, 'error': 'timeout'}
        except httpx.NetworkError:
            return {'url': url, 'error': 'network'}
        except Exception:
            return {'url': url, 'error': 'unknown'}

    async def close(self):
        await self._client.aclose()
