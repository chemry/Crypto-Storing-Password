from getpass import getpass, getuser
import db_utils as db
import hash_utils as pw

INPUT_STR = ' ' * 8 + '> '
OUTPUT_STR = ' ' * 8

def printBanner():
    print("""
        ****************************************
        *    Welcome to Crypto Application!    *
        ****************************************""")


def printMenu():
    print("""
        1. Register
        2. Login
        3. Quit""")

def printMethod():
    print("""
        1. Plaintext (Very Dangerous!)
        2. Pure SHA-256 (Still Dangerous)
        3. SHA-512 with salt and rounds""")

def printLog(output):
    print(OUTPUT_STR + output)


def getUserPass():
    username = input(OUTPUT_STR + "Please enter your username: ")
    password = getpass(OUTPUT_STR + "Please enter your password (password will be hidden): ")
    return username, password


def register():
    username, password = getUserPass()
    if not db.checkUsername(username):
        printLog("Username Already Exists!")
        return

    # hs = pw.sha512(password)
    # print(hs)
    # pw.verify_sha512(password, hs)
    printMethod()
    option = getOption([1, 2, 3])
    if option == 1:
        password = pw.plain(password)
    elif option == 2:
        password = pw.sha256(password)
    elif option == 3:
        password = pw.sha512(password)

    db.insertUser(username, password)
    printLog("Success!")



def login():
    username, password = getUserPass()
    store = db.getPassword(username)
    if len(store) == 0:
        printLog("Loing Failed!")
        return
    store = store[0][1]
    # print(store)
    if not pw.verify(password, store):
        printLog("Login Failed!")
        return
    printLog("Success!")


def getOption(valid):
    try:
        option = input(INPUT_STR).strip()
        if len(option) == 0:
            return getOption(valid)
        if option in valid:
            return option
        option = int(option)
        if option in valid:
            return option        
        raise(ValueError)
    except ValueError:
        printLog("That's not a valid option!")
        return getOption(valid)

def main():
    
    printBanner()

    while True:
        printMenu()
        option = getOption([1, 2, 3, 'q', 'debug'])
        if option in [3, 'q']:
            db.quit()
            printLog("Bye!")
            break
        elif option == 1:
            register()
        elif option == 2:
            login()
        elif option == 'debug':
            db.printAll()
    



if __name__ == "__main__":
    db.prepareDB()
    main()