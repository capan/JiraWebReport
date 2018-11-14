# -*- coding: utf-8 -*-
from collections import Counter
import collections
import os
from jira import JIRA
import sys
import datetime as d
from calculation import calculate
import time
import psycopg2

user_name = 'username'
password = 'secret'
mail_password = 'secret'
project_list = []
assg_list = []
priority_list = []
state_list = []
yy_ank_project_list = []
yy_ank_assg_list = []
yy_ank_priority_list = []
yy_ank_state_list = []
# ig_ank_project_list = []
# ig_ank_assg_list = []
# ig_ank_priority_list = []
# ig_ank_state_list = []
yy_ist_project_list = []
yy_ist_assg_list = []
yy_ist_priority_list = []
yy_ist_state_list = []
state_list = []
assignee_list = []
unassigned_list = []
satis_cat = []
months = ['', u'ocak', u'subat', u'mart', u'nisan', u'mayis', u'haziran',
          u'temmuz', u'agustos', u'eylul', u'ekim', u'kasim', u'aralik']
calculator = calculate()

# Jira Server Connection
options = {
    'server': 'http://projeportal.netcad.com.tr:8080'}
# Jira Auth
try:
    jira = JIRA(options, basic_auth=(f'{user_name}', f'{password}'))
except BaseException as Be:
    print(Be)
props = jira.application_properties()
print(f'Jira Authentication Başarılı. . .({d.datetime.now()})')
now = d.datetime.now()
# DB Auth
conn = psycopg2.connect(
    "dbname=jiraReportDb user=localhost  password=1 port=5432")
conn.autocommit = True
cur = conn.cursor()
start_time = time.time()
########################### JIRA QUERIES ###########################
# All issues in a month. If written as startOfMonth(-1) issues of the last month will be queried.
all_issues = jira.search_issues(
    'created > startOfMonth(-1) AND created < endOfMonth(-1)', maxResults=False
)

# All closed issues of the last month
all_closed_issues = jira.search_issues(
    '(resolution = Çözüldü or resolution = "Daha Sonra Çözülecek" or resolution = "İptal Edildi"  or resolution = Mükerrer  or resolution = "Yeniden Tekrarlanamadı" or resolution = "İptal Edildi")  and created > startOfMonth(-1) AND created < endOfMonth(-1) order by createdDate  asc', maxResults=False
)
# YY-Ankara Issues
yy_ankara_issues = jira.search_issues(
    'created > startOfMonth(-1) AND created < endOfMonth(-1) and category = YY-Ankara', maxResults=False
)
# # IG-Ankara Issues
# ig_ankara_issues = jira.search_issues(
#     'created > startOfMonth(-1) AND created < endOfMonth(-1) and category = IG-Ankara', maxResults=False
# )
# YY-İstanbul Issues
yy_istanbul_issues = jira.search_issues(
    'created > startOfMonth(-1) AND created < endOfMonth(-1) and category = YY-İstanbul', maxResults=False)

print("---Query Time:  %s seconds ---" % (time.time() - start_time))


def jiraQueryHandler(jiraQuery, priorityList, stateList, projectList, assgList):
    for i in range(0, len(jiraQuery)):
        priorityList.append(jiraQuery[i].raw[u'fields'][u'priority'][u'name'])
        stateList.append(jiraQuery[i].raw[u'fields'][u'status'][u'name'])
        projectList.append(jiraQuery[i].fields.project.name)
        try:
            assgList.append(jiraQuery[i].raw[u'fields'][u'assignee'][u'name'])
        except BaseException as Be:
            assgList.append('N/A')


# All Issues List
jiraQueryHandler(all_issues, priority_list,
                 state_list, project_list, assg_list)
# YY Ankara List
jiraQueryHandler(yy_ankara_issues, yy_ank_priority_list,
                 yy_ank_state_list, yy_ank_project_list, yy_ank_assg_list)
# # IG-Ankara Lists
# jiraQueryHandler(ig_ankara_issues, ig_ank_priority_list,
#                  ig_ank_state_list, ig_ank_project_list, ig_ank_assg_list)
# YY-İstanbul Lists
jiraQueryHandler(yy_istanbul_issues, yy_ist_priority_list,
                 yy_ist_state_list, yy_ist_project_list, yy_ist_assg_list)


# Creating Tables

cur.execute(
    f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = '{str(months[now.month-1].lower())}_rapor')")
rows = cur.fetchall()
if rows[0][0] is True:
    x = input(f' {str(months[now.month-1].lower())} ayına ait tablolar daha önceden oluşturulmuş. \n Programın çalışması için bu tabloların silinip yeniden oluşturulması gerekiyor. \n Tabloların otomatik olarak silinip yeniden oluşturulmasını istiyorsanız e yazıp enter a basın: ')
    if x != 'e':
        print('Programdan çıkıldı')
        sys.exit()
    else:
        cur.execute(
            f'DROP TABLE IF EXISTS {str(months[now.month-1].lower())}_rapor')
        cur.execute(
            f'DROP TABLE IF EXISTS {str(months[now.month-1].lower())}_rapor_ayrinti')
        cur.execute(
            f'DROP TABLE IF EXISTS {str(months[now.month-1].lower())}_ank_ayrinti')
        cur.execute(
            f'DROP TABLE IF EXISTS {str(months[now.month-1].lower())}_ist_ayrinti')
else:
    pass

cur.execute(
    f"CREATE TABLE IF NOT EXISTS {str(months[now.month-1].lower())}_rapor (id SERIAL,grup varchar(30), miktar integer)")
print(f'{str(months[now.month-1].lower())}_rapor tablosu oluşturuldu')

cur.execute(
    f"CREATE TABLE IF NOT EXISTS {str(months[now.month-1].lower())}_ank_ayrinti (id SERIAL,degisken varchar(255), miktar integer, etiket varchar(255))")
print(f'{str(months[now.month-1].lower())}_ank_ayrinti tablosu oluşturuldu')

cur.execute(
    f"CREATE TABLE IF NOT EXISTS {str(months[now.month-1].lower())}_ist_ayrinti (id SERIAL,degisken varchar(255), miktar integer, etiket varchar(255))")
print(f'{str(months[now.month-1].lower())}_ist_ayrinti tablosu oluşturuldu')

cur.execute(
    f"CREATE TABLE IF NOT EXISTS {str(months[now.month-1].lower())}_rapor_ayrinti (id SERIAL,degisken varchar(255), miktar integer, etiket varchar(255))")
print(f'{str(months[now.month-1].lower())}_rapor_ayrinti tablosu oluşturuldu')

print('ok')

cur.execute(
    f"INSERT INTO {str(months[now.month-1].lower())}_rapor (grup, miktar) values ('ToplamYYAnkara',{len(yy_ankara_issues)})")
cur.execute(
    f"INSERT INTO {str(months[now.month-1].lower())}_rapor (grup, miktar) values ('ToplamYYİstanbul',{len(yy_istanbul_issues)})")
cur.execute(
    f"INSERT INTO {str(months[now.month-1].lower())}_rapor (grup, miktar) values ('Toplam',{len(yy_ankara_issues)+len(yy_istanbul_issues)})")
cur.execute(
    f"INSERT INTO {str(months[now.month-1].lower())}_rapor (grup, miktar) values ('OrtalamaTalep',{calculator.meantime(all_closed_issues):1.2f})")
cur.execute(
    f"INSERT INTO {str(months[now.month-1].lower())}_rapor (grup, miktar) values ('MedianTalep',{calculator.mediantime(all_closed_issues)})")


def turkifyList(theList):
    for x in range(0, len(theList)):
        for x in range(0, len(theList)):
            if u'Resolved' == theList[x][0]:
                theList[x] = tuple(
                    [u'Çözüldü', theList[x][1]])
            elif u'Closed' == theList[x][0]:
                theList[x] = tuple(
                    [u'Kapandı', theList[x][1]])
            elif u'Waiting for support' == theList[x][0]:
                theList[x] = tuple(
                    [u'Destek Bekleniyor', theList[x][1]])
            elif u'Waiting for customer' == theList[x][0]:
                theList[x] = tuple(
                    [u'Müşteriden Yanıt Bekleniyor', theList[x][1]])
            elif u'On Hold' == theList[x][0]:
                theList[x] = tuple(
                    [u'Beklemede', theList[x][1]])
    return theList


yy_ank_priorty_count = turkifyList(Counter(yy_ank_priority_list).most_common())
yy_ank_state_count = turkifyList(Counter(yy_ank_state_list).most_common())
yy_ank_project_count = turkifyList(Counter(yy_ank_project_list).most_common())
yy_ank_assignee_count = turkifyList(Counter(yy_ank_assg_list).most_common())

for x in range(0, len(yy_ank_priorty_count)):
    cur.execute(
        f"INSERT INTO {str(months[now.month-1].lower())}_ank_ayrinti (degisken, miktar,etiket) values ('{yy_ank_priorty_count[x][0]}',{yy_ank_priorty_count[x][1]},'priority')")

for x in range(0, len(yy_ank_state_count)):
    cur.execute(
        f"INSERT INTO {str(months[now.month-1].lower())}_ank_ayrinti (degisken, miktar,etiket) values ('{yy_ank_state_count[x][0]}',{yy_ank_state_count[x][1]},'state')")

for x in range(0, len(yy_ank_project_count)):
    cur.execute(
        f"INSERT INTO {str(months[now.month-1].lower())}_ank_ayrinti (degisken, miktar,etiket) values ('{yy_ank_project_count[x][0]}',{yy_ank_project_count[x][1]},'project')")

for x in range(0, len(yy_ank_assignee_count)):
    cur.execute(
        f"INSERT INTO {str(months[now.month-1].lower())}_ank_ayrinti (degisken, miktar,etiket) values ('{yy_ank_assignee_count[x][0]}',{yy_ank_assignee_count[x][1]},'assignee')")


yy_ist_priorty_count = turkifyList(Counter(yy_ist_priority_list).most_common())
yy_ist_state_count = turkifyList(Counter(yy_ist_state_list).most_common())
yy_ist_project_count = turkifyList(Counter(yy_ist_project_list).most_common())
yy_ist_assignee_count = turkifyList(Counter(yy_ist_assg_list).most_common())

for x in range(0, len(yy_ist_priorty_count)):
    cur.execute(
        f"INSERT INTO {str(months[now.month-1].lower())}_ist_ayrinti (degisken, miktar,etiket) values ('{yy_ist_priorty_count[x][0]}',{yy_ist_priorty_count[x][1]},'priority')")

for x in range(0, len(yy_ist_state_count)):
    cur.execute(
        f"INSERT INTO {str(months[now.month-1].lower())}_ist_ayrinti (degisken, miktar,etiket) values ('{yy_ist_state_count[x][0]}',{yy_ist_state_count[x][1]},'state')")

for x in range(0, len(yy_ist_project_count)):
    cur.execute(
        f"INSERT INTO {str(months[now.month-1].lower())}_ist_ayrinti (degisken, miktar,etiket) values ('{yy_ist_project_count[x][0]}',{yy_ist_project_count[x][1]},'project')")

for x in range(0, len(yy_ist_assignee_count)):
    cur.execute(
        f"INSERT INTO {str(months[now.month-1].lower())}_ist_ayrinti (degisken, miktar,etiket) values ('{yy_ist_assignee_count[x][0]}',{yy_ist_assignee_count[x][1]},'assignee')")

priorty_count = turkifyList(Counter(priority_list).most_common())
state_count = turkifyList(Counter(state_list).most_common())
project_count = turkifyList(Counter(project_list).most_common())
assignee_count = turkifyList(Counter(assg_list).most_common())

userMeanSolution = calculator.personalinsight(all_closed_issues)

for x in range(0, len(priorty_count)):
    cur.execute(
        f"INSERT INTO {str(months[now.month-1].lower())}_rapor_ayrinti (degisken, miktar,etiket) values ('{priorty_count[x][0]}',{priorty_count[x][1]},'priority')")

for x in range(0, len(state_count)):
    cur.execute(
        f"INSERT INTO {str(months[now.month-1].lower())}_rapor_ayrinti (degisken, miktar,etiket) values ('{state_count[x][0]}',{state_count[x][1]},'state')")

for x in range(0, len(project_count)):
    cur.execute(
        f"INSERT INTO {str(months[now.month-1].lower())}_rapor_ayrinti (degisken, miktar,etiket) values ('{project_count[x][0]}',{project_count[x][1]},'project')")

for x in range(0, len(assignee_count)):
    cur.execute(
        f"INSERT INTO {str(months[now.month-1].lower())}_rapor_ayrinti (degisken, miktar,etiket) values ('{assignee_count[x][0]}',{assignee_count[x][1]},'assignee')")

for x in range(0, len(userMeanSolution)):
    cur.execute(
        f"INSERT INTO {str(months[now.month-1].lower())}_rapor_ayrinti (degisken, miktar,etiket) values ('{userMeanSolution[x][0]}',{userMeanSolution[x][1]},'user_mean')")
