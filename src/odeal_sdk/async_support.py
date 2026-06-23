"""
Odeal SDK Async Desteği.

Mevcut senkron BaseResource'u async/await ile kullanılabilir hale getirir.
stdlib asyncio + concurrent.futures kullanır — ek bağımlılık gerektirmez.

Kullanım:
    import asyncio

    async def main():
        config = OdealConfig(secret_key='sk_xxx', merchant_key='mk_xxx')
        client = OdealClient(config)
        
        # Tek async istek
        result = await run_async(client.basket.create_basket, request)
        
        # Paralel istekler
        results = await asyncio.gather(
            run_async(client.basket.create_basket, req1),
            run_async(client.basket.create_basket, req2),
            run_async(client.basket.create_basket, req3)
        )

    asyncio.run(main())
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import TypeVar, Callable, Any

T = TypeVar('T')

# Global thread pool (SDK geneli paylaşımlı)
_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix='odeal-async')


async def run_async(func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    """
    Senkron SDK metodunu async olarak çalıştırır.
    
    ThreadPoolExecutor kullanarak IO-blocking çağrıyı non-blocking yapar.
    Mevcut event loop'un executor'ünü kullanır.
    
    Args:
        func: Çağrılacak senkron metot (ör. client.basket.create_basket).
        *args: Metoda geçilecek pozisyonel argümanlar.
        **kwargs: Metoda geçilecek anahtar argümanlar.
    
    Returns:
        Metodun dönüş değeri.
    
    Example:
        result = await run_async(client.basket.create_basket, request)
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, lambda: func(*args, **kwargs))


async def run_parallel(*calls: tuple) -> list:
    """
    Birden fazla SDK çağrısını paralel olarak çalıştırır.
    
    Args:
        *calls: (func, *args) tuple'ları.
    
    Returns:
        Sonuçların listesi (çağrı sırasına göre).
    
    Example:
        results = await run_parallel(
            (client.basket.create_basket, req1),
            (client.basket.create_basket, req2),
        )
    """
    tasks = [run_async(call[0], *call[1:]) for call in calls]
    return await asyncio.gather(*tasks)
