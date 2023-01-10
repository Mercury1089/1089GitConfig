'''
Rohan Shah
Swap between pre-stored git credentials
'''

import csv
from subprocess import Popen, PIPE


def git_config(user_email, user_name):
    email_cmd = Popen(['git', 'config', '--local', 'user.email', user_email], stdout=PIPE, stderr=PIPE)
    stdout, stderr = email_cmd.communicate()
    name_cmd = Popen(['git', 'config', '--local', 'user.name', user_name], stdout=PIPE, stderr=PIPE)

def git_reset():
    reset_email = Popen(['git', 'config', '--local', '--unset', 'user.email'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = reset_email.communicate()
    reset_name = Popen(['git', 'config', '--local', '--unset', 'user.name'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = reset_name.communicate()
    return stdout.decode('utf-8')

def save_creds(user_email, user_name):
    HEADERS = ['GitHub Username', 'GitHub Email']
    with open('creds.csv', 'a') as Creds:
        writer = csv.DictWriter(Creds, fieldnames=HEADERS)
        writer.writerow({
            HEADERS[0]: user_name,
            HEADERS[1]: user_email
        })

def get_users():
    usernames = []
    with open('creds.csv', 'r') as Creds:
        reader = csv.DictReader(Creds)
        for column in reader:
            usernames.append(column['GitHub Username'])
    return usernames

def select_user():
    users = get_users()
    username = input("Enter username (case-sensitive): ")
    if username in users:
        return username
    print("\nUSERNAME NOT FOUND, SELECT FROM BELOW\n")
    for index, user in enumerate(users):
        print("({}) {} ".format(index, user))
    ind = int(input('Enter number: '))
    try:
        return users[ind]
    except IndexError:
        return users[0] # default to master account

def fetch_data(username):
    with open('creds.csv', 'r') as Creds:
        reader = csv.DictReader(Creds)
        for column in reader:
            if column['GitHub Username'] == username:
                return [column['GitHub Email'], username]


def main():
    directions = input("Would you like to (1) LOGIN TO GIT, (2) RESET/LOGOUT, (3) STORE NEW CREDENTIALS: ")
    if int(directions) == 2:
        return git_reset()  
    if int(directions) == 3:
        name = input("""Find the Github Account Name (NOT username):
        1). Visit www.github.com/{username}/ 
        2). Select the bold name (most likely your full name)
        
        Enter GitHub name: """)
        email = input("""Find the GitHub Git Operations email
        1). Settings --> Emails
        2). <some_id>+username@users.noreply.github.com
        
        Enter GitHub email: """)
        save_creds(email, name)
        return
    user = select_user()
    data = fetch_data(user)
    git_config(*data)

main()