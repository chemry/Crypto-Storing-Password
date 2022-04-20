import sqlite3
conn = sqlite3.connect('crypt.db')

def prepareDB():
    cur = conn.cursor()
    sql = 'create table if not exists user (username text, password text)'
    cur.execute(sql)
    conn.commit()
    return conn

def checkUsername(username):
    cur = conn.cursor()
    # print(username)
    cur.execute('select * from user where username = (?)', (username,))
    # print(cur.fetchall())
    return len(cur.fetchall()) == 0


def insertUser(username, password):
    cur = conn.cursor()
    cur.execute('insert into user values (?,?)', (username, password))
    conn.commit()


def getPassword(username):
    cur = conn.cursor()
    cur.execute('select * from user where username = ?', (username, ))
    return cur.fetchall()


def printAll():
    cur = conn.cursor()
    cur.execute('select * from user')
    for entry in cur.fetchall():
        print(entry)
    # print(cur.fetchall())


def quit():
    conn.commit()
    conn.close()