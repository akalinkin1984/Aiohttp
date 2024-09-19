import json

from aiohttp import web
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncAttrs
from pydantic import ValidationError

from models import Session, Advertisement, engine, init_orm
from schema import CreateAdv, UpdateAdv


app = web.Application()


async def orm_context(app):
    print('START')
    await init_orm()
    yield
    await engine.dispose()
    print('FINISH')


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


def get_http_error(error_cls, msg: str | dict | list):
    return error_cls(
        text=json.dumps(
            {'error': msg},
        ),
        content_type='application/json'
    )


async def get_adv(adv_id: int, session: AsyncAttrs) -> Advertisement:
    adv = await session.get(Advertisement, adv_id)
    if adv is None:
        raise get_http_error(web.HTTPNotFound, 'The advertisement not found')
    return adv


async def add_adv(adv: Advertisement, session: AsyncAttrs) -> Advertisement:
    session.add(adv)
    try:
        await session.commit()
    except IntegrityError:
        raise get_http_error(web.HTTPConflict, 'The advertisement already exists')
    return adv


def validate_json(json_data: dict, schema_cls: type[CreateAdv] | type[UpdateAdv]):
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
    except ValidationError as err:
        errors = err.errors()
        for error in errors:
            error.pop('ctx', None)
        raise web.HTTPBadRequest


class AdvView(web.View):
    @property
    def adv_id(self):
        return int(self.request.match_info['adv_id'])

    @property
    def session(self):
        return self.request.session

    async def get(self):
        adv = await get_adv(self.adv_id, self.session)
        return web.json_response(adv.json)

    async def post(self):
        adv_data = validate_json(await self.request.json(), CreateAdv)
        adv = Advertisement(**adv_data)
        adv = await add_adv(adv, self.session)
        return web.json_response({'status': 'The advertisement is posted', 'id': adv.id})

    async def patch(self):
        adv_data = validate_json(await self.request.json(), UpdateAdv)
        adv = await get_adv(self.adv_id, self.session)
        for field, value in adv_data.items():
            setattr(adv, field, value)
        adv = await add_adv(adv, self.session)
        return web.json_response({'status': 'The advertisement is update', 'id': adv.id})

    async def delete(self):
        adv = await get_adv(self.adv_id, self.session)
        await self.session.delete(adv)
        await self.session.commit()
        return web.json_response({'status': 'The advertisement is deleted'})


app.add_routes([
    web.post('/adv/', AdvView),
    web.get('/adv/{adv_id:\d+}/', AdvView),
    web.patch('/adv/{adv_id:\d+}/', AdvView),
    web.delete('/adv/{adv_id:\d+}/', AdvView),
])

web.run_app(app)
