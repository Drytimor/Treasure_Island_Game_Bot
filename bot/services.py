import asyncio
import logging
from sqlalchemy import insert, update, select, delete
from sqlalchemy.exc import IntegrityError
from decimal import Decimal
from contextlib import suppress
from config.database import db_session
from models import (
    Users,
    Currencies,
    Teams,
    Rates,
    Wallet
)

log = logging.getLogger(__name__)


async def create_user(user_id, username):
    async with db_session() as s:
        if not await s.get(Users, user_id):
            stmt = insert(Users).values(
                id=user_id,
                username=username,
                tris=100,
                gold=0,
                farm_gold=0
            )
            await s.execute(stmt)
            await s.commit()


async def get_user(user_id):
    log.info(f'Getting user {user_id}')
    async with db_session() as s:
        user = await s.get(Users, user_id)
        return user


async def get_well_tris():
    async with db_session() as s:
        currencies = await s.get(Currencies, 'Tris')
        return currencies.well


async def exchange_tris_for_gold(number_tris, user_id):
    async with db_session() as s:
        well = await get_well_tris()
        stmt = (
            update(Users)
            .where(Users.id == user_id)
            .values(
                tris=(Users.tris - Decimal(number_tris)),
                gold=(Users.gold + (Decimal(number_tris) * well))
            )
            .returning(Users.id)
        )
        result = await s.execute(stmt)
        await s.commit()
        return result


async def create_a_bit(user_id, team, amount_gold):
    async with db_session() as s:
        stmt_teams = (
            update(Teams)
            .where(Teams.name == team)
            .values(gold=Teams.gold + Decimal(amount_gold))
        )
        stmt_users = (
            update(Users)
            .where(Users.id == user_id)
            .values(gold=Users.gold - Decimal(amount_gold))
        )
        stmt_check_rates = (
            select(Rates.id)
            .where(Rates.user_id == user_id, Rates.team_name == team)
        )
        result = await s.execute(stmt_check_rates)
        if result.first():
            stmt_rates = (
                update(Rates)
                .where(Rates.user_id == user_id)
                .values(
                    gold=Rates.gold + Decimal(amount_gold)
                )
                .returning(Rates.id)
            )
        else:
            stmt_rates = (
                insert(Rates)
                .values(
                    user_id=user_id,
                    team_name=team,
                    gold=Decimal(amount_gold)
                )
                .returning(Rates.id)
            )
        await s.execute(stmt_teams)
        await s.execute(stmt_users)
        result = await s.execute(stmt_rates)
        await s.commit()
        return result


async def get_total_amount_gold_teams():
    async with db_session() as s:
        stmt_total_amount_gold = (
            select(Teams.gold)
        )
        result = await s.scalars(stmt_total_amount_gold)
        total_amount_gold = sum(result)
        return total_amount_gold


async def sending_result_to_users():
    async with db_session() as s:
        stmt_total_amount_gold_teams = (
            select(Teams)
            .order_by(-Teams.gold)
        )
        result_win = await s.scalars(stmt_total_amount_gold_teams)
        winner, two, three = result_win.all()

        stmt_rates_win = (
            select(Rates)
            .where(Rates.team_name == winner.name)
        )
        stmt_results_losers = (
            select(Rates)
            .where(Rates.team_name != winner.name)
        )

        result_win = await s.scalars(stmt_rates_win)
        result_los = await s.scalars(stmt_results_losers)

        dict_result_win_users = {
            'winner': {},
            'losser': {}
        }

        for row in result_win.all():
            user_winner_gold_with_10 = row.gold + (row.gold / 100 * 10)
            dict_result_win_users['winner'][row.user_id] = user_winner_gold_with_10
            dict_result_win_users['winner'].setdefault('team', row.team_name)
            stmt = (
                update(Users)
                .where(Users.id == row.user_id)
                .values(
                    farm_gold=Users.farm_gold + user_winner_gold_with_10)
                )

            await s.execute(stmt)

        sum_gold_los_teams = 0

        for row in result_los.all():
            dict_result_win_users['losser'][row.user_id] = row.team_name
            sum_gold_los_teams += row.gold

        stmt_refill_well = (
            update(Wallet)
            .where(Wallet.id == 1)
            .values(total_amount=Wallet.total_amount + sum_gold_los_teams)
        )

        stmt_clear_rates = (
            delete(Rates)
        )

        stmt_clear_gold_teams = (
            update(Teams)
            .values(gold=0)
        )

        await s.execute(stmt_clear_gold_teams)
        await s.execute(stmt_clear_rates)
        await s.execute(stmt_refill_well)

        await s.commit()

        return dict_result_win_users



