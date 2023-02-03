import sqlite3 as sq


def sql_start():
    """
    Подключение к бд и создание таблицы menu если такая не создана в бд
    :return: None
    """
    global base, cur
    base = sq.connect('testMenu.db')
    cur = base.cursor()
    if base:
        print('data base connect')
    base.execute('CREATE TABLE IF NOT EXISTS menu'
                 '(id INTEGER PRIMARY KEY UNIQUE, '
                 'first_name TEXT, '
                 'balance INTEGER DEFAULT 0, '
                 'status_in_menu TEXT)')
    base.commit()


async def sql_add_user(state):
    """
    Добавление пользователя в бд, когда тот вызывает меню у бота
    :param state: tuple(Integer, Sting, Integer, Sting)
    :return: None
    """
    cur.execute('INSERT OR REPLACE INTO menu VALUES (?, ?, ?, ?)', state)
    base.commit()


async def message_all_user(element):
    """
    Выборка всей бд
    :param element: String
    :return: None
    """
    return cur.execute(f'SELECT * FROM menu WHERE status_in_menu = ?', (element, )).fetchall()


async def sql_read_for_balance(element):
    """
    Выборка одного элемента по индефикатору
    :param element: Integer
    :return: None
    """
    return cur.execute(f'SELECT * FROM menu WHERE id = ?', (element, )).fetchone()
