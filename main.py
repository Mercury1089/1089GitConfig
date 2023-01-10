"""
Tool for swapping between multiple git credentials
================================
Rohan Shah, Team Mercury 1089
"""

import csv
import sys
import argparse
from subprocess import Popen, PIPE

class GitCustomizer1089():
    def __init__(self):
        parser = argparse.ArgumentParser(
            description="1089's command-line tool for fast git config",
            usage="""1089git <command> [<args>]
Available commands:
save-creds    Save git <username, email> for future use
reset         Clean the current git config
users         List all the available users
login         Login using a pre-saved username
""")
        parser.add_argument("command", help="command to run")
        if len(sys.argv) < 2:
            parser.print_help()
            return
        args = parser.parse_args([sys.argv[1].replace('-','_')])
        if not hasattr(self, args.command):
            print('Unrecognized command\n')
            parser.print_help()
            return
        getattr(self, args.command)()

    def reset(self):
        print("\n===== RESETTING GIT BACK TO DEFAULT =====\n")
        self._reset()

    def users(self):
        print("\n===== STORED USERS =====\n")
        usernames = self._users()
        for user in usernames:
            print(user)

    def login(self):
        print("===== LOGIN =====")
        user = self._select_user()
        self._git_config(*self._fetch_data(user))

    def save_creds(self):
        print("\n===== SAVING CREDENTIALS =====\n")
        print("""GITHUB ACCOUNT NAME:
1). Visit www.github.com/{username}
2). Select the bold name (most likely your full name)
""")
        name = input("Enter GitHub Account Name: ")
        print("""GITHUB OPERATIONS EMAIL
Used for web-based GitHub Operations

1). GitHub Settings --> Emails
2). <some_id>+username@users.noreply.github.com
""")
        email = input("Enter GitHub Email: ")
        self._save_creds(email, name)
        
    def _git_config(self, user_email, user_name):
        '''
        Update git config with desired values

        :param user_email: GitHub email used for web-based operations
        :param user_name: GitHub Account Name
        '''
        email_cmd = Popen(['git', 'config', '--local', 'user.email', user_email], stdout=PIPE, stderr=PIPE)
        stdout, stderr = email_cmd.communicate()
        name_cmd = Popen(['git', 'config', '--local', 'user.name', user_name], stdout=PIPE, stderr=PIPE)

    def _reset(self):
        '''
        Remove git config --local entries (if any)
        '''
        reset_email = Popen(['git', 'config', '--local', '--unset', 'user.email'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = reset_email.communicate()
        reset_name = Popen(['git', 'config', '--local', '--unset', 'user.name'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = reset_name.communicate()
        return stdout.decode('utf-8')


    def _save_creds(self, user_email, user_name):
        '''
        Write credentials into CSV

        :param user_email: GitHub email used for web-based operations
        :param user_name: GitHub Account Name
        '''
        HEADERS = ['GitHub Username', 'GitHub Email']
        with open('creds.csv', 'a') as Creds:
            writer = csv.DictWriter(Creds, fieldnames=HEADERS)
            writer.writerow({
                HEADERS[0]: user_name,
                HEADERS[1]: user_email
            })

    def _users(self):
        '''
        Read CSV and return list of usernames
        '''
        usernames = []
        with open('creds.csv', 'r') as Creds:
            reader = csv.DictReader(Creds)
            for column in reader:
                usernames.append(column['GitHub Username'])
        return usernames

    def _select_user(self):
        '''
        Use user input to select a pre-existing username
        '''
        users = self._users()
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

    def _fetch_data(self, username):
        '''
        Match username to email
        '''
        with open('creds.csv', 'r') as Creds:
            reader = csv.DictReader(Creds)
            for column in reader:
                if column['GitHub Username'] == username:
                    return [column['GitHub Email'], username]

def main():
    GitCustomizer1089()

main()