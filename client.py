import asyncio
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            'http://0.0.0.0:8080/adv',
            json={'title': 'Холодильник',
                  'description': 'Отличный холодильник',
                  'owner': 'Иван'}
        )

        # response = await session.get(
        #     'http://0.0.0.0:8080/adv/56',
        # )

        # response = await session.patch(
        #     'http://0.0.0.0:8080/adv/6',
        #     json = {'title': 'Телевизор',
        #             'description': 'Хороший телевизор',
        #             }
        # )

        # response = await session.delete(
        #     'http://0.0.0.0:8080/adv/3',
        # )

        print(response.status)
        print(await response.text())


asyncio.run(main())

# import requests
#
#
# response = requests.post(
#     'http://0.0.0.0:8080/adv',
#     json = {'title': 'Холодильник',
#             'description': 'Отличный холодильник',
#             'owner': 'Иван'},)
#
# print(response.status_code)
# print(response.json())