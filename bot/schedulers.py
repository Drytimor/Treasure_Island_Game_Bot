from services import sending_result_to_users
import logging
import enum

team_name = {
    'Tartugi': 'Пираты Тартуги',
    'Jamajki': 'Пираты Ямайки',
    'Berberes': 'Пираты Берберес'
}


log = logging.getLogger(__name__)


async def send_message_users(bot):
    users = await sending_result_to_users()
    if users.get('winner'):
        team_win = users['winner'].pop('team')
        for user, gold in users['winner'].items():
            await bot.send_message(user, text=f'{team_name[team_win]} выиграли\nтвой доход: {round(gold, 4)} gold')

        for user, team in users['losser'].items():
            await bot.send_message(user, text=f'{team_name[team]} проиграли')

