# 1089GitConfig
1089's git config tool for fast git account login

## Setup

1. Clone the repository
2. Link an alias to the script
    ```
    alias 1089git='python3 Users/username/git/1089GitConfig/main.py'
    ```
    
3. See Usage below



## Usage

```
HHS-702-23:1089GitConfig s9800826$ 1089git
usage: 1089git <command> [<args>]
Available commands:
save-creds    Save git <username, email> for future use
reset         Clean the current git config
users         List all the available users
login         Login using a pre-saved username

1089's command-line tool for fast git config

positional arguments:
  command     command to run

optional arguments:
  -h, --help  show this help message and exit
```
