import urllib2, re
from datetime import datetime, timedelta
from pushbullet import PushBullet
from operator import itemgetter
import sqlite3

conn = sqlite3.connect('../db.sqlite3')
c = conn.cursor()

key = "PwmEg59jL6KjS2N0e6BjX3IEs2LpadYs"
pb = PushBullet(key)

for user in c.execute('SELECT * FROM register_user'):
    print user
    leerlingnummer = user[3]
    url = "http://gepro.nl/roosters/rooster.php?leerling=" + str(
        leerlingnummer) + "&type=Leerlingrooster&afdeling=schooljaar2014-2015_OVERIG&wijzigingen=1&school=1814"
    htmlPage = urllib2.urlopen(url).read()

    lastChangedPat = re.compile('([0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9] [0-9]+:[0-9][0-9]:[0-9][0-9])')
    dateStr = re.search(lastChangedPat, htmlPage).group()
    date = datetime.strptime(dateStr, "%d-%m-%Y %H:%M:%S")
    db_date = datetime.strptime(str(user[2]), "%Y-%m-%d %H:%M:%S.%f")
    if date - db_date < timedelta():
        print "nothing new for " + str(leerlingnummer)
        continue

    c.execute("UPDATE register_user SET updated=? WHERE number=?", (str(datetime.now()), leerlingnummer))
    conn.commit()

    pb_users = [i for i in pb.contacts if i.name == str(leerlingnummer)]
    for pb_user in pb_users:
        print pb_user
        parts = []
        stage = 0
        changePat = re.compile('class="tableCell(New|Removed)">(y([0-9]+)|[a-z]+)')
        hourPat = re.compile('width="50" class="tableHeader">([0-9])e uur')
        dayPat = re.compile('<td align="left" width="auto" class="tableCell">')

        for change in re.finditer(changePat, htmlPage):
            if change.group(1) == "Removed":
                parts.append([change.group(2)])
                for tempHour in re.finditer(hourPat, htmlPage[:change.start()]):
                    hour = tempHour
                parts[-1].append(hour.group(1))
                day = re.findall(dayPat, htmlPage[hour.end():change.start()])
                parts[-1].append(len(day))
            else:
                stage += 1
                if stage == 1:
                    parts.append([change.group(2)])
                else:
                    parts[-1].append(change.group(2))
                if stage == 3:
                    stage = 0
                    for tempHour in re.finditer(hourPat, htmlPage[:change.start()]):
                        hour = tempHour
                    parts[-1].append(hour.group(1))
                    day = re.findall(dayPat, htmlPage[hour.end():change.start()])
                    parts[-1].append(len(day))

        days = ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag"]
        text = ""
        parts = sorted(parts, key=itemgetter(-1))
        for part in parts:
            text += str(days[part[-1]-1]) + " " + part[-2] + "e uur "
            if len(part) == 5:
                text += part[0] + " " + part[1] + " " + part[2] + "\n"
            else:
                text += part[0] + "\n"
        if text == "":
            text = "Geen roosterwijzigingen"

        print text
        success, push = pb_user.push_note("Rooster wijzigingen", text)

conn.close()
