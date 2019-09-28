import requests
from bs4 import BeautifulSoup

import time
import os

def send_message(message):
    message = str(message)
    message = "'" + message + "'"
    command = "notify-send " + message
    os.system(command)

def poll():
    cred_file = open("Credentials.txt","r")
    content = cred_file.readlines()
    line1 = content[0].rstrip()
    cred_file.close()

    ctr_file = open("Counter.txt","r")
    counter = ctr_file.readlines()[0].rstrip()
    counter = int(counter)
    ctr_file.close()

    username = line1.split(",")[0]
    password = line1.split(",")[1]

    login_data = {}
    login_data["username"] = username
    login_data["password"] = password

    with requests.Session() as sess:
        url = "https://online.iitg.ac.in/tnp/Main.jsp"

        try:
            r = sess.post(url,login_data)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            send_message("Check Internet Connection!!")
            return
        except requests.exceptions.ConnectionError as err:
            send_message("Check Internet Connection!!")
            return

        jobs = sess.get("https://online.iitg.ac.in/tnp/student/job_eligible_list.jsp")
        soup =  BeautifulSoup(jobs.text,"html5lib")

        tables = soup.select('table')
        
        if len(tables) == 0:
            send_message("Incorrect Credentials!!")
            return

        table = tables[0]
        rows = table.select('tr')

        ctr = 0
        for row in rows:
            if len(row.select('td')) > 0:
                ctr += 1
        
        if ctr > counter:
            ctr_file = open("Counter.txt","w")
            ctr_file.write(str(ctr))
            ctr_file.close()
            
            message_string = str(ctr-counter)
            message_string = message_string + " companies added.\n"
            send_message(message_string)
    

while(True):
    poll()
    time.sleep(10)