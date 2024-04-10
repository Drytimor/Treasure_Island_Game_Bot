from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder,
    ReplyKeyboardMarkup,
    InlineKeyboardBuilder,
    InlineKeyboardMarkup
)


def main_menu_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Игра", callback_data="start_game")],
            [InlineKeyboardButton(text="Кошелек", callback_data="wallet")]
        ]
    )
    return keyboard


def get_wallet_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Обменять Tris", callback_data="tris_exchange")],
            [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
        ]
    )
    return keyboard


def get_back_wallet_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="wallet")]
        ]
    )
    return keyboard


def get_back_bet_on_team():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="start_game")]
        ]
    )
    return keyboard


def get_choices_team_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Пираты Ямайки", callback_data="Jamajki")],
                         [InlineKeyboardButton(text="Пираты Берберес", callback_data="Berberes")],
                         [InlineKeyboardButton(text="Пираты Тартуги", callback_data="Tartugi")],
                         [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]]
    )
    return keyboard




