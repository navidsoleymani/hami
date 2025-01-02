import contextlib
import json
import logging
import random

import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ApplicationBuilder, CallbackQueryHandler, CommandHandler, CallbackContext

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARNING
)

# this is backend endpoint.
API_BASE_ADDRESS = 'http://127.0.0.1:8000'


class DB(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DB, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    goal_table = {}
    follower_count_table = {}

    def add(self, table_name, **kwargs):
        from uuid import uuid4

        table = getattr(self, table_name)
        id_ = str(uuid4())
        table[id_] = kwargs
        return id_

    def remove(self, table_name, id_):
        try:
            table = getattr(self, table_name)
            del table[id_]
        except:
            pass

    def get(self, table_name, id_):
        try:
            table = getattr(self, table_name)
            return table[id_]
        except:
            return None

    def get_list(self, table_name, **filters):
        table = getattr(self, table_name)
        if not filters:
            return table
        tmp = []
        for k, v in table.items():
            for fk, fv in filters.items():
                if v[fk] == fv:
                    v['user_id'] = v['instagram_id']
                    tmp.append(v)
        return tmp


def add_goal_endpoint(*args, **kwargs):
    return f'{API_BASE_ADDRESS}/api/v1/ssa/goals/add/'


def add_goal(*args, **kwargs):
    return DB().add('goal_table', **kwargs)


def delete_goal_endpoint(goal_id, *args, **kwargs):
    return f'{API_BASE_ADDRESS}/api/v1/ssa/goals/delete/{goal_id}/'


def delete_goal(goal_id, *args, **kwargs):
    return DB().remove('goal_table', goal_id)


def all_goals_endpoint(*args, **kwargs):
    return f'{API_BASE_ADDRESS}/api/v1/ssa/goals/getlist/'


def all_goals(*args, **kwargs):
    return DB().get_list('goal_table')


def get_user_goals_endpoint(t_id, *args, **kwargs):
    return f'{API_BASE_ADDRESS}/api/v1/ssa/goals/getlist/{t_id}/'


def get_user_goals(t_id, *args, **kwargs):
    return DB().get_list('goal_table', t_id=t_id)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    initial message when user hit `Start` button
    """
    hello_msg = '''Hi {}
        Commands:

        /show_goals
        /add_goal Username follower_count, example: /add_goal navid 1000
    '''
    await update.message.reply_text(hello_msg.format(update.effective_user.first_name))


async def show_goals_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    handler to show currently set goals for a telegram user
    """
    keyboard = []
    # resp = requests.get(get_user_goals_endpoint(t_id=update.effective_user.id)).json()
    resp = get_user_goals(t_id=update.effective_user.id)
    for i in resp:
        keyboard.append([InlineKeyboardButton(f"{i['user_id']} - {i['follower_count']}",
                                              callback_data=json.dumps({}))])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"You currently Set Goals: {len(keyboard)}", reply_markup=reply_markup)


async def add_goal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    a simple handler that add a new goal
    """
    with contextlib.suppress(Exception):
        # requests.post(
        #     add_goal_endpoint(),
        #     data={
        #         't_id': update.effective_user.id,
        #         'instagram_id': context.args[0],
        #         'follower_count': int(context.args[1])})
        add_goal(**{
            't_id': update.effective_user.id,
            'instagram_id': context.args[0],
            'follower_count': int(context.args[1])})
        await update.message.reply_text("Tracking Goal added")
        return

    await update.message.reply_text(f"Sorry, something went wrong...")


async def buttons_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    a simple handler for buttons in bot chats.
    we do nothing here, but we can configure it for multiple actions based on update.callback_query data
    """
    query = update.callback_query
    await query.answer()
    q_data = json.loads(query.data)


async def tracking_job(context: CallbackContext) -> None:
    """
    this function periodically fetch goals from API and check if user hit any
    """
    # goals = requests.get(all_goals_endpoint()).json()
    goals = all_goals()
    for goal in goals:
        with contextlib.suppress(Exception):
            # here instead of random.randint we can make an actual call to Instagram or Twitter
            # endpoints and query given user's follower count or anything else
            # here we just use a random generator to show how we can send message to engaged users in telegram Bot API
            if random.randint(0, 100) > 50:
                await context.bot.send_message(
                    chat_id=goal['telegram_user'],
                    text=f"{goal['user_id']} has more than '"
                         f"{goal['follower_count']} followers now!")


if __name__ == '__main__':
    # replace it with your own token
    token = "7864397213:AAGxbVkfJ-6ZDP8UPFPuUoATXSBhCSAlQFg"
    app = ApplicationBuilder().token(token).build()
    start_handler = CommandHandler('start', hello)
    app.add_handler(CallbackQueryHandler(buttons_callback))
    app.add_handler(CommandHandler('add_goal', add_goal_handler))
    app.add_handler(CommandHandler('show_goals', show_goals_handler))
    app.add_handler(start_handler)
    job_que = app.job_queue
    # run every 10 seconds, 10 second after bot startup
    job_que.run_repeating(tracking_job, interval=10, first=10)
    app.run_polling()
