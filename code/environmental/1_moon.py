import ephem
import datetime
import csv

with open(r'./moon.csv', 'a', newline="", encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(['Day','Light','Phase'])


date = datetime.datetime(2017, 1, 1)

for i in range(1826):
    next = ephem.next_new_moon(date)
    previous = ephem.previous_new_moon(date)  

    e_date = ephem.date(date)
    
    far = min(e_date-previous,next-e_date)

    until = next-e_date

    if until < 1.855 or until > 27.745:
        phase = 'New Moon'
    elif until > 1.855 and until <= 5.555:
        phase = 'Waning Crescent'
    elif until > 5.555 and until <= 9.265:
        phase = 'Third Quarter'
    elif until > 9.265 and until <= 12.975:
        phase = 'Waning Gibbous'
    elif until > 12.975 and until <= 16.628:
        phase = 'Full Moon'
    elif until > 16.628 and until <= 20.395:
        phase = 'Waxing Gibbous'
    elif until > 20.395 and until <= 24.105:
        phase = 'First Quarter'
    else:
        phase = 'Waxing Crescent'


    

    with open(r'./moon.csv', 'a', newline="", encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow([date,far,phase])
    

    date += datetime.timedelta(days=1)