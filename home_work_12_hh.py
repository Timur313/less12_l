
# coding: utf-8

# In[1]:


import re
import json
import requests
from pprint import pprint


# In[2]:


area_id = 88
text_val = 'Python разработчик'

DOMAIN = 'https://api.hh.ru/'

url_vacancies = f'{DOMAIN}vacancies'
url_areas = f"{DOMAIN}areas/{area_id}"


# In[3]:


stat_info = {
    "salary_min": [],
    "salary_max": [],
    "requirement": {}
}

f_str = lambda x_str: re.sub("[^A-Za-z]", "", x_str.strip()).lower()
n_full_req = 0

page_i = 1
while page_i < 1e5:
    
    params = {
        'text': text_val,
        'page': page_i,
        'area': area_id
    }
    
    result = requests.get(url_vacancies, params=params).json()
    
    print(f"{page_i} / {result['pages']}")
    print(len(result["items"]))
    
    for item in result['items']:
    
        if item['salary']:
            if item['salary']['from']:
                stat_info['salary_min'].append(item['salary']['from'])
            if item['salary']['to']:
                stat_info['salary_max'].append(item['salary']['to'])
                
        s_test = item['snippet']['requirement']
        req_list_rem = [s for s in re.sub("[^A-Za-z#+]", " ", s_test.strip()).split() if s]
        
        for req_i in req_list_rem:
            if len(req_i) > 2:
                n_full_req += 1
            
                req_rem = f_str(req_i)
                if req_rem in stat_info['requirement'].keys():
                    stat_info['requirement'][req_rem]["count"] += 1
                else:
                    stat_info['requirement'].update({
                        req_rem: {
                            "count": 1,
                            "init_name": req_i
                            }
                    })
                    
    page_i += 1
    if page_i > result['pages']:
        break
        
        
stat_info["salary_min"] = round(sum(stat_info["salary_min"]) / len(stat_info["salary_min"]), 2)
stat_info["salary_max"] = round(sum(stat_info["salary_max"]) / len(stat_info["salary_max"]), 2)

for rk in stat_info['requirement'].keys():
    stat_info['requirement'][rk]['count'] = f"{round( stat_info['requirement'][rk]['count'] / n_full_req * 100, 1 )}%"


# In[4]:


with open("result.json", "w", encoding = 'UTF-8') as f:
    json.dump(stat_info, f, indent=4,  ensure_ascii=False)

