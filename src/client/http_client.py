import httpx
import asyncio


class AsyncHTTPClient:
    """
    Асинхронный HTTP-клиент, использует httpx. Выполняет запросы конкурентно

    Attributes:
        max_concurrent_tasks (int): Максимальное количество задач, работающих конкурентно
        max_keepalive_connections (int): Максимальноек количество открытых соединений
        timeout (float): Макс время выполнения каждого запроса, после которого он будет закрыт
    """
    def __init__(self,
                 timeout: float = 3.0,
                 max_concurrent_tasks: int = 100,
                 max_keepalive_connections: int = 10):

        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            limits=httpx.Limits(max_keepalive_connections=max_keepalive_connections),
            follow_redirects=True
        )
        self._semaphore = asyncio.Semaphore(max_concurrent_tasks)

    async def get(self, url: str) -> dict:
        """ Создает GET запрос к url и возвращает время ответа и статус код """
        async with self._semaphore:
            try:
                loop = asyncio.get_running_loop()
                start = loop.time()
                response = await self._client.get(url)
                elapsed = loop.time() - start
                return {
                    'url': url,
                    'elapsed': elapsed,
                    'status_code': response.status_code
                }
            except httpx.TimeoutException:
                return {'url': url, 'error': 'timeout'}
            except httpx.NetworkError:
                return {'url': url, 'error': 'network'}
            except Exception:
                return {'url': url, 'error': 'unknown'}

    async def close(self):
        """ Закрывает соединение и освобождает ресурсы """
        await self._client.aclose()

    async def __aenter__(self):
        """Вход в контекстный менеджер (async with)"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Выход из контекстный менеджер (async with)"""
        await self.close()
