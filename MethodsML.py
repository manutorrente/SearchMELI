import gspread
import time
import smtplib as mail


def get_date():
    f = '%Y-%m-%d %H:%M'
    now = time.localtime()
    return time.strftime(f, now)


def send_mail(sender, password, to, subject, message):
    con=mail.SMTP("smtp.gmail.com", 587)
    con.ehlo()
    con.starttls()
    con.login(sender, password)
    con.sendmail(sender, to, f"Subject: {subject}\n\n{message}\n\n")
    
    
def open_sheet(file, worksheet, json_file):
    gc = gspread.service_account(filename=json_file)
    sheet=gc.open(file)
    worksheet=sheet.get_worksheet(worksheet)
    return worksheet

