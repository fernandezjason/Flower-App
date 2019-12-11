Current status of Assignment 5:
- All base functionality complete for 100% on assignment

Needs:
- Error handling for user input (ie check if flower they want to edit is in DB)
    - ie. check if date entered correctly
- Any extra credit we want to do


Link database using:
$ python3
$ from flowers import db
$ db.create_all()
$ exit()

You can check that the tables are there properly:
$ sqlite3 flowers2019.db
>> .tables
>> .dump FLOWERS
>> .exit

TO RUN:
$ python3 flowersdb.py

then open 127.0.0.1.5000
