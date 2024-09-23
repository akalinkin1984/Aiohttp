import asyncio
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            'http://127.0.0.1:8080/adv/',
            json={'title': 'Telephone',
                  'description': 'Iphone',
                  'owner': 'Petya'}
        )

        # response = await session.get(
        #     'http://127.0.0.1:8080/adv/1/',
        # )

        # response = await session.patch(
        #     'http://127.0.0.1:8080/adv/1/',
        #     json = {'title899': 'New Telephone',
        #             'description111': 'New Iphone',
        #             }
        # )

        # response = await session.delete(
        #     'http://127.0.0.1:8080/adv/1/',
        # )

        print(response.status)
        print(await response.text())


asyncio.run(main())
