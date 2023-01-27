import imaplib
import os
import email 
import json 
import sys
import mysql.connector
import html2text
import socket
import time
import datetime
import tkinter as tk
import pandas as pd
import threading
import logging
import time

limit = 5
mail_password = {}
imap_servers = {}
connections = {}
threads = []
logfile = 'C:/Users/Dell/Desktop/Email_attachment_extractor/logfile.txt'
with open(logfile,'w') as f:
    pass
# socket.setdefaulttimeout(15)

#wpfxmopnmzxmxlqu
#qyohxxpkemhqslzq

def already_logged_in():
    # f = open('mail_password.csv','w')
    df = pd.read_csv('mail_password.csv')
    print(df)
    if df.empty:
        return 0
    for i in range(df.shape[0]):
        mail_password[df.iloc[i]['username']] = df.iloc[i]['password']
        imap_servers[df.iloc[i]['username']] = df.iloc[i]['imap']
    return 1

def add_user(username, password, host='imap.gmail.com'):
    if username in mail_password:
        return 'Already Logged in'
    elif len(mail_password) == 5:
        return 'Maximum Limit of emails reached'
    else:
        try:
            print(username,password,host)
            connection = imaplib.IMAP4_SSL(host, 993)
            if connection.login(username, password):
                mail_password[username] = password
                connections[username] = connection
                imap_servers[username] = host
                with open('mail_password.csv','a') as f:
                    f.write(username+','+password+','+host+'\n')
                return 'Successfully Logged in!'
            else:
                return 'Invalid Credentials!'
        except socket.timeout:
            return 'Timeout Error! Check network speed and firewall settings.'
        except: 
            return 'Failed to establish connection! Check network connection or imap server.'

def display_users():
    return mail_password.keys()

def remove_user(username):
    if username in mail_password:
        mail_password.pop(username)
        imap_servers.pop(username)
        print(mail_password)
        return 'We shall no longer extract attachments from '+username
    else:
        return 'Invalid Email!'

def cleanup():
    with open('mail_password.csv','w') as f:
        f.write('username,password,imap\n')
        for i in mail_password:
            print(i)
            f.write(i+','+mail_password[i]+','+imap_servers[i]+'\n')
    return

#Can this be converted into a generator??
#Hopefully
def display_messages(username, filters):
    if username in mail_password:
        connection = connections[username]
        _, totmails = connection.select('inbox')
        set_of_mails = set()
        list_of_msgs = list()
        read = filters['UNSEEN']
        for filter in filters:
            if filter == 'DATE' or filter == 'UNSEEN':
                continue
            for value in filters[filter]: 
                vals = set()
                #print(f'{filter} "{value}"')
                status, data = connection.search(None, f'{filter} "{value}"', 'UNSEEN') if read else connection.search(None, f'{filter} "{value}"')
                #print(1 if data[0].decode().split() else 0)
                if status == 'OK':
                    vals = data[0].decode().split()
                else:
                    continue
                if not set_of_mails:
                    set_of_mails = set_of_mails.union(vals)
                else:
                    set_of_mails = set_of_mails.intersection(vals)
        #return set_of_mails
        #print('set of mails',set_of_mails)
        while set_of_mails:
            _, data = connection.fetch(set_of_mails.pop(), '(RFC822)')
            data = email.message_from_bytes(data[0][1])
            msg = {}
            for header in ['SUBJECT', 'FROM', 'TO', 'DATE']:
                msg[header] = data[header]
            for part in data.walk():
                if part.get('Content-Disposition') is None:
                    msg['content'] = part.get('Content-Disposition')
                    msg['body'] = part.get_payload(decode = True)
                    print(part.get('Content-Disposition'))
                    #print(html2text.html2text(msg['body']))
            list_of_msgs.append(msg.decode())
        return list_of_msgs
    else:
        return []

def get_attachments(filters, location, location_filter,thread_no):
    connection = []
    user_email = {}
    users = []
    for i,user in enumerate(mail_password):
        if filters['usernames'][i]:
            con = imaplib.IMAP4_SSL(imap_servers[user],993)
            print(con)
            con.login(user,mail_password[user])
            connection.append(con)
            users.append(user)
    for index, i in enumerate(connection):
        _, totmails = i.select('inbox')
        set_final1 = set()
        set_final2 = set()
        if 'From' in filters:
            for value in filters['From']: 
                vals = set()
                set_of_mails = set()
                #print(f'{filter} "{value}"')
                status, data = i.search(None, f"FROM '{value}'", 'UNSEEN') if filters['UNSEEN'] else i.search(None, f'FROM "{value}"')
                print(status, 1 if data[0].decode().split() else 0)
                if status == 'OK':
                    vals = data[0].decode().split()
                    set_of_mails = set_of_mails.union(vals)
                set_final1 = set_final1.union(set_of_mails) 
        print(set_final1) 
        if 'Subject' in filters:
            for value in filters['Subject']:
                vals = set()
                set_of_mails = set()
                status,data = i.search(None, f'SUBJECT "{value}"', 'UNSEEN') if filters['UNSEEN'] else i.search(None, f'SUBJECT "{value}"')
                if status == 'OK':
                    vals = data[0].decode().split()
                    set_of_mails = set_of_mails.union(vals)
                set_final2 = set_final2.union(set_of_mails)
            if set_final1:
                set_final1 = set_final1.intersection(set_final2)
            else:
                set_final1 = set_final1.union(set_final2)
        #set_final1 = apply_other_filters(i,set_final1,filters)

        d = {'1':'Jan','2':'Feb','3':'Mar','4':'Apr','5':'May','6':'Jun', '7':'Jul', '8':'Aug', '9':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}
        vals = set()
        start_date = filters['Start_date'].split('/')
        start_date = start_date[1] + '-' +  d[start_date[0]] + '-' + start_date[2]
        end_date = filters['End_date'].split('/')
        end_date = end_date[1] + '-' +  d[end_date[0]] + '-' + end_date[2]
        if start_date == end_date:
            status, data = i.search(None, f'Since "{start_date}"')
        else:
            status, data = i.search(None, f'Since "{start_date}"', f'Sentbefore "{end_date}"')
        vals = data[0].decode().split()
        if set_final1:
            set_final1 = set_final1.intersection(vals)
        else:
            set_final1 = set(vals)
        print('before download',set_final1)
        user_email[users[index]] = set_final1
        for user in user_email:
            set_of_mails = user_email[user]
            while set_of_mails:
                _, data = i.fetch(set_of_mails.pop(), '(RFC822)')
                data = email.message_from_bytes(data[0][1])
                # print('Here')
                for part in data.walk():
                    print(part.get('Content-Disposition'))
                    if part.get('Content-Disposition') is not None:
                        attchName = part.get_filename()
                        print(attchName)
                        if bool(attchName):
                            if location_filter:
                                if location_filter in data:
                                    fil = (data[location_filter].split(':')[-1].split('<')[0]).strip(' ')
                                    attchFilePath = location+str("/")+fil+str("/") 
                                else:
                                    attchFilePath = location+str("/")+location_filter+str("/")
                            else:
                                attchFilePath = location+str("/")
                            print(str(attchName).split('.'))
                            if (('all' in filters['Type']) or (str(attchName).split('.')[-1].lower() in filters['Type'])):
                                print('before failure',attchFilePath)
                                os.makedirs(os.path.dirname(attchFilePath), exist_ok=True)
                                attchFilePath = attchFilePath +str(attchName)
                                print(attchFilePath)
                                with open(attchFilePath, "wb") as f:
                                    f.write(part.get_payload(decode=True))
                                with open(logfile,'a') as f:
                                    f.write('\n'+str(thread_no)+','+attchFilePath)
    with open(logfile,'a') as f:
        f.write('\n'+str(thread_no)+','+'Download_complete')
    return user_email


def download(filters, location, location_filter):
    if(len(threads) == 3):
        for i in threads:
            if not i.is_alive():
                threads.remove(i)        
    if len(threads) == 3:
        return "Wait for other downloads to complete!"
    x = threading.Thread(target=get_attachments, args=(filters, location, location_filter, len(threads)+1), daemon=True)
    threads.append(x)
    print('Here 1')
    x.start()
    print('Here 2')
    return "Download Started"

if __name__ == '__main__':
    print('Test Case ID: UT-01:',add_user('amoghgs123@gmail.com','wpfxmopnmzxmxlqu'))
    # print('Test Case #4: ',end = "")
    print('Test Case ID: UT-02:',add_user('amogh123@gmail.com','123'))
    # print('Test Case #2: ',end = "")
    print('Test Case ID: UT-03:',remove_user('amoghgs123@gmail.com'))
    add_user('amoghgs123@gmail.com','wpfxmopnmzxmxlqu')
    #for i in display_messages('amoghgs123@gmail.com',{'From':["bigadata"], 'Subject':["Spark"], "UNSEEN": 0}):
    #    print(html2text.html2text(i['body'].decode()))
    #print('Test Case ID: UT-06:',get_attachments('amoghgs123@gmail.com',{'From':["bigadata"], 'Subject':["Spark"], "UNSEEN": 0}))
    print(get_attachments({'Start_date': '11/12/2022', 'End_date':'11/12/2022', 'From':['bigadata','google'], 'Subject':['Assignment 3'],'usernames':[1], 'UNSEEN':0}))
