from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from contextlib import suppress
from pymongo.errors import DuplicateKeyError
from bson.decimal128 import Decimal128, create_decimal128_context
from decimal import localcontext


async def create_collections():
    cluster = AsyncIOMotorClient(host='localhost', port=27017)
    db = cluster.gameBot
    teams = db['teams']
    users = db['users']
    currencies = db['currencies']
    rates = db['rates']
    with localcontext(create_decimal128_context()) as ctx:
        gold = Decimal128(ctx.create_decimal("0"))
        well = Decimal128(ctx.create_decimal("100"))

    currencies.insert_one(
        {"_id": "Tris", "well": well}
    )
    teams.insert_many([
        {'_id': 'Jamajki', 'name': 'Пираты Ямайки', 'gold': gold},
        {'_id': 'Berberes', 'name': 'Пираты Берберес', 'gold': gold},
        {'_id': 'Tartugi', 'name': 'Пираты Тартуги', 'gold': gold}
    ])


if __name__ == '__main__':
    asyncio.run(create_collections())


