#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import csv

def get_json(url):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0'}
    job_json=requests.post(url,headers=headers)
    return job_json.text

def parse_json(job_json):
    job=json.loads(job_json)
    page_size=len(job.get('content').get('result'))
    total_page_count=job.get('content').get('totalPageCount')
    company_list=[]
    for i in range(page_size):
        company_name=job.get('content').get('result')[i].get('companyShortName')
        position_name=job.get('content').get('result')[i].get('positionName')
        salary=job.get('content').get('result')[i].get('salary')
        company_list.append(company_name)
        company_list.append(position_name)
        company_list.append(salary)
    return company_list,total_page_count

init_url='http://www.lagou.com/jobs/positionAjax.json?px=new&city=广州&kd=python'
company_all_list=[]
url=init_url+'&pn='+str(1)
job_json=get_json(url)
company_list,total_page_count=parse_json(job_json)
company_all_list.extend(company_list)
page_no=total_page_count
for i in range(2,page_no+1):
    url = init_url + '&pn=' + str(i)
    job_json = get_json(url)
    company_list, total_page_count = parse_json(job_json)
    company_all_list.extend(company_list)

with open('../lagou/lagou.csv','w+') as csvfile:
    csvwriter=csv.writer(csvfile)
    for i in range(0,len(company_all_list)+1,3):
        csvwriter.writerow(company_all_list[i:i+3])