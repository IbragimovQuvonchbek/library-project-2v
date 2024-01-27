import dotenv
from scripts.conn import connection

dotenv.load_dotenv()


def user_exists(username, gmail):
    conn = connection()
    cursor = conn.cursor()
    query = "SELECT id FROM users WHERE username = %s or gmail = %s"
    value = (username, gmail)
    cursor.execute(query, value)
    result = cursor.fetchall()
    conn.close()
    return len(result) != 0


def read_users_table():
    conn = connection()
    cursor = conn.cursor()
    query = "SELECT * FROM users"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result


def signup(name, surname, username, gmail, password):
    conn = connection()
    cursor = conn.cursor()
    query = "INSERT INTO users (name, surname, username ,gmail, password, superuser) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (name, surname, username, gmail, password, True if not read_users_table() else False)
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return read_users_table()[-1][0]


def login(username, password):
    conn = connection()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    values = (username, password)
    cursor.execute(query, values)
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else -1


def is_superuser(user_id):
    conn = connection()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = %s"
    values = (user_id,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    conn.close()
    return result[-1]


def show_all_books():
    conn = connection()
    cursor = conn.cursor()
    query = "SELECT id, name FROM books where unit >= 1 order by id"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result


def read_books_table():
    conn = connection()
    cursor = conn.cursor()
    query = "SELECT * FROM books where unit >= 1 order by id"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result


def search_books(keyword):
    keyword = keyword.strip()
    books_data = read_books_table()
    raw_data = []
    for book in books_data:
        if keyword.lower() in book[1].lower():
            raw_data.append((book[0], book[1]))
    return raw_data


def get_registered_books(user_id):
    conn = connection()
    cursor = conn.cursor()
    query = '''
    select b.id, b.name from books as b
    join ownedbooks o on b.id = o.book_id where o.user_id = %s order by b.id;
    '''
    values = (user_id,)
    cursor.execute(query, values)
    result = cursor.fetchall()
    conn.close()
    return result


def search_registered_books(keyword: str, data):
    keyword = keyword.strip()
    if keyword.strip():
        raw_data = []
        for book in data:
            if keyword.lower() in book[1].lower():
                raw_data.append((book[0], book[1]))
        return raw_data
    else:
        return data


def get_book_by_id(book_id):
    conn = connection()
    cursor = conn.cursor()
    query = '''
    select * from books where id = %s;
    '''
    values = (book_id,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    conn.close()
    return result


def is_book_registered(user_id, book_id):
    conn = connection()
    cursor = conn.cursor()
    query = '''
    select * from ownedbooks where user_id = %s and book_id = %s;
    '''
    values = (user_id, book_id)
    cursor.execute(query, values)
    result = cursor.fetchall()
    conn.close()
    return len(result) != 0


def delete_book(book_id):
    conn = connection()
    cursor = conn.cursor()
    query = '''
    delete from books where id = %s;
    '''
    values = (book_id,)
    cursor.execute(query, values)
    conn.commit()
    conn.close()


def add_book(name, author, category, description, unit):
    conn = connection()
    cursor = conn.cursor()
    query = "INSERT INTO books (name, author, category , description, unit) VALUES (%s, %s, %s, %s, %s)"
    values = (name, author, category, description, unit)
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    return read_books_table()[-1][0]


def show_users():
    conn = connection()
    cursor = conn.cursor()
    query = "SELECT id, name from users where superuser = false"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result


def search_users(keyword):
    keyword = keyword.strip()
    users_data = show_users()
    raw_data = []
    for user in users_data:
        if keyword.lower() in user[1].lower():
            raw_data.append((user[0], user[1]))
    return raw_data


def get_user_by_id(user_id):
    conn = connection()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = %s"
    values = (user_id,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    conn.close()
    return result


def get_user_books_info(user_id):
    conn = connection()
    cursor = conn.cursor()
    query = '''
    select b.name from books as b join ownedbooks as o 
    on b.id = o.book_id where o.user_id = %s;
    '''
    values = (user_id,)
    cursor.execute(query, values)
    result = cursor.fetchall()
    conn.close()
    return result


def register_book(user_id, book_id):
    conn = connection()
    cursor = conn.cursor()

    query = "select unit from books where id = %s"
    values = (book_id,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    if result and result[0] >= 1:
        query1 = "INSERT INTO ownedbooks (user_id, book_id) VALUES (%s, %s)"
        values1 = (user_id, book_id)
        cursor.execute(query1, values1)
        conn.commit()

        query2 = "update books set unit = unit - 1 where id = %s"
        values2 = (book_id,)
        cursor.execute(query2, values2)
        conn.commit()
    conn.close()


def unregister_book(user_id, book_id):
    conn = connection()
    cursor = conn.cursor()
    query1 = "delete from ownedbooks where user_id = %s and book_id = %s"
    values1 = (user_id, book_id)
    cursor.execute(query1, values1)
    conn.commit()

    query2 = "update books set unit = unit + 1 where id = %s"
    values2 = (book_id,)
    cursor.execute(query2, values2)
    conn.commit()
    conn.close()


def edit_book(name, author, category, description, unit, book_id):
    book = get_book_by_id(book_id)
    updated_name = book[1]
    updated_author = book[2]
    updated_category = book[3]
    updated_description = book[4]
    updated_unit = book[5]
    if name and name != 'leave it for unchanged':
        updated_name = name.strip()
    if author and author != 'leave it for unchanged':
        updated_author = author.strip()
    if category and category != 'leave it for unchanged':
        updated_category = category.strip()
    if description and description != 'leave it for unchanged':
        updated_description = description.strip()
    if unit and unit != 'leave it for unchanged':
        updated_unit = unit

    conn = connection()
    cursor = conn.cursor()
    query1 = "update books set name = %s, author = %s, category = %s, description = %s, unit = %s where id = %s"
    values1 = (updated_name, updated_author, updated_category, updated_description, updated_unit, book_id)
    cursor.execute(query1, values1)
    conn.commit()
    conn.close()
