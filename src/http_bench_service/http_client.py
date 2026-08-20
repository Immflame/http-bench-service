import httpx
import asyncio
import time

class AsyncHTTPClient:
    def __init__(self,
                 timeout: float = 3.0,
                 max_concurrent_tasks: int = 100,
                 max_keepalive_connections: int = 10):

        self.__client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            limits=httpx.Limits(max_keepalive_connections=max_keepalive_connections),
            follow_redirects=True
        )
        self.__semaphore = asyncio.Semaphore(max_concurrent_tasks)

    async def get(self, url: str) -> dict:
        async with self.__semaphore:
            try:
                start = time.perf_counter()
                response = await self.__client.get(url)
                time_duration = time.perf_counter() - start
                return {
                    'url': url,
                    'time_duration': time_duration,
                    'status_code': response.status_code
                }
            except httpx.TimeoutException:
                return {'url': url, 'error': 'timeout'}
            except httpx.NetworkError:
                return {'url': url, 'error': 'network'}
            except Exception:
                return {'url': url, 'error': 'unknown'}

    async def close(self):
        await self.__client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
