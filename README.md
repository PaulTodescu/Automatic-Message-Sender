# Automatic Message Sender

## Initial setup

Step 0

Install Python 3.7 (at least) and Git from https://www.python.org/downloads/, respectively https://git-scm.com/downloads

Step 1

Clone this project by running
```bash
git clone https://github.com/LupulescuAlexandru/Automatic-Message-Sender.git
```

Step 2

Open a terminal from the root of the project and run 

```bash
python -m venv env
```
Step 3

Now run 

WINDOWS
```bash
cd env/scripts && activate && cd .. && cd .. && pip install -r req.txt
```
LINUX/MACOS
```bash
source env/bin/activate && pip install -r req.txt
```

Step 4

Run migrations
```bash
cd app && python manage.py migrate
```

Step 5

To run the server run
```bash
python manage.py runserver
```

That's it!
## Opening the server (after initial setup)

From the project root (where run_me_windows.bat is located), run from a terminal
```bash
run_me_windows
```
If you're on Linux/MacOS, activate env, go inside app folder and run python manage.py runserver

By default, you can view the app from http://127.0.0.1:8000
