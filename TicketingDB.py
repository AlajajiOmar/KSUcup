import sqlite3
import csv
import datetime


def createDB():
    conn = sqlite3.connect('test.db')

    conn.execute('''CREATE TABLE ACCOUNT
        (AID TEXT PRIMARY KEY,
        type TEXT NOT NULL,
        name TEXT NOT NULL,
        password TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT NOT NULL);''')
    conn.execute('''CREATE TABLE EVENT
        (EID TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        date_time TEXT NOT NULL,
        capacity INT NOT NULL,
        AID TEXT NOT NULL,
        booking_number INT NOT NULL,
        foreign key (AID) references ACCOUNT(AID)
            );''')
    conn.execute('''CREATE TABLE BOOKING
        (SID TEXT  NOT NULL,
        EID TEXT NOT NULL, 
        constraint house_items_pk primary key (SID, EID),
        constraint SID_fk foreign key (SID) references ACCOUNT(AID),
        constraint EID_fk foreign key (EID) references EVENT(EID));'''
                 )

    conn.execute(
        '''insert into ACCOUNT values ('1234567890', 'admin', 'mohammed','18138372fad4b94533cd4881f03dc6c69296dd897234e0cee83f727e2e6b1f63',0512345678,'admin@ksu.edu.sa');''')
    conn.commit()


def writeEvent(id, name, location, capacity, time, aid, booking_number):
    conn = sqlite3.connect('test.db')
    conn.execute(
        f'''insert into EVENT values ('{id}', '{name}','{location}', '{time}', '{capacity}', '{aid}', '{booking_number}');''')
    conn.commit()
    a = conn.execute('''select * from EVENT''')
    conn.close()


def checkExist(id):
    conn = sqlite3.connect('test.db')
    events_record = conn.execute('''select * from EVENT''')
    a = list(events_record)
    if a == []:
        return True
    for i in events_record:
        if i[0] == str(id):
            return False
    conn.close()
    return True


def backUP():
    conn = sqlite3.connect('test.db')
    accounts_record = conn.execute('''select * from ACCOUNT''')
    events_record = conn.execute('''select * from EVENT''')
    booking_record = conn.execute('''select * from BOOKING''')
    with open("backup.csv", 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['ACCOUNT'])
        csv_writer.writerows(accounts_record)

        csv_writer.writerow(['EVENT'])
        csv_writer.writerows(events_record)

        csv_writer.writerow(['BOOKING'])
        csv_writer.writerows(booking_record)
    conn.close()


def activeEvent():
    conn = sqlite3.connect('test.db')
    events_record = conn.execute('''select EID, name, location, date_time from EVENT''')
    active_events = list()
    for i in events_record:
        if is_future(i[3]):
            id = "ID: " + str(i[0])
            name = "Name: " + str(i[1])
            location = "Location: " + str(i[2])
            date = "Date: " + str(i[3])
            active_events.append(f"{id}, {name}, {location}, {date}")

    conn.close()
    return active_events


def is_future(d2):
    t = datetime.datetime.today()
    s = d2.split(" ")
    x = datetime.datetime.strptime(s[0], "%Y-%m-%d")
    return x >= datetime.datetime.strptime(t.strftime("%Y-%m-%d"), "%Y-%m-%d")


def activeBokings(id):
    conn = sqlite3.connect('test.db')
    a = conn.execute(f'''select EVENT.name ,EVENT.LOCATION,EVENT.date_time from BOOKING,EVENT 
    where SID = '{id}'and  BOOKING.EID = EVENT.EID
    ''')
    active = []
    for i in a:
        if is_future(i[2]):
            active.append(i)
    conn.close()
    return active


def book(id, eid):
    conn = sqlite3.connect('test.db')
    a = conn.execute(f'''select EID from EVENT 
       where EID = '{eid}' and capacity != booking_number
       ''')
    if list(a) == []:
        conn.close()
        return 'Sorry event is fully booked'
    try:
        conn.execute(f'''insert into BOOKING VALUES ('{id}','{eid}') ''')
    except:
        conn.close()
        return 'already booked'

    conn.execute(f'''update EVENT set booking_number = booking_number+1 where EID = '{eid}' ''')
    conn.commit()
    conn.close()
    return 'your booking is confirmed'


def createSAccount(id, name, pas, ph, em):
    conn = sqlite3.connect('test.db')
    try:
        # a = conn.execute('select AID from ACCOUNT Where AID={};'.format(id))
        conn.execute(f'''insert into ACCOUNT values ('{id}','student','{name}','{pas}','{ph}','{em}');''')
        conn.commit()
        conn.close()
        return True

    except:
        conn.commit()
        conn.close()
        return False


def loginS(id, pas):
    conn = sqlite3.connect('test.db')
    a = conn.execute(f'''select AID from ACCOUNT Where AID='{id}';''')
    if list(a) == []:
        conn.close()
        return 'account does not exist'
    a = conn.execute(f'''select AID from ACCOUNT Where AID='{id}' and password='{pas}';''')
    if list(a) == []:
        conn.close()
        return 'Wrong password'
    a = conn.execute(f'''select type from ACCOUNT Where AID='{id}' and password='{pas}';''')
    x = list(a)[0][0]
    conn.close()
    return x


if __name__ == '__main__':
    '''
    IMPORTANT !!!!
    Run this ONLY once
    to make your life easier :)
    we already have an admin (inside createDB function)
    his info: 
    ID: 1234567890, Password: qwe123
    
    After this run sign up
    '''
    createDB()

