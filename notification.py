import pandas
import pywhatkit
import datetime
import smtplib

my_email = "dhwnaitsal@gmail.com"
password = "DhwnaitM@4125"


def absent_students():
    data = pandas.read_csv("records.csv")
    all_words = data.to_dict(orient='records')
    phone = []
    email = []
    list_of_absent = []
    for i in all_words:
        if i['present'] != "P":
            rollno = i['rollno']
            name = i['name']
            email.append(i['email'])
            list_of_absent.append(f"{rollno} - {name}")
    for i in range(len(email)):
        with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
            # with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=email[i],
                msg="Subject:ABSENT!\n\nYou didn't attend today's class. Try to be regular"
            )
    return list_of_absent
    # now = datetime.datetime.now()
    # for i in range(len(phone)):
    #     send_time = now + datetime.timedelta(minutes=i)
    #     hour = send_time.hour
    #     minute = send_time.minute
    #     print(minute)
    #     minute = minute+3
    #     phone_number = f"+{phone[i]}"
    #     print(phone_number)
    #     pywhatkit.sendwhatmsg(phone_number, message="*You didn't attend today's class. Try to be regular!!*",time_hour=hour, time_min=minute)


# absent_students()
