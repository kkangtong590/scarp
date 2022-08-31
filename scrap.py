from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

print("1번 페이지부터 n번 페이지 까지 스크랩")
n=int(input("n:"))

url = 'https://m.dcinside.com/board/umamusu?headid=160&page={}'

table = pd.DataFrame()
header = {
    'Referer':'https://www.dcinside.com/',
    'User-Agent':'Mozilla/5.0 (Linux; Android 9; ASUS_X00TD; Flow) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/359.0.0.288 Mobile Safari/537.36'
}
list_type=[]
list_amount=[]
list_user=[]

for p in range(1,n+1):
    res = requests.get(url.format(p), headers=header)
    soup = BeautifulSoup(res.text, 'html.parser')
    a = soup.find_all("div", {"class": "gall-detail-lnktb"})
    u = soup.find_all("span", {"class": "blockInfo"})
    for i in range(len(a)):
        j=a[i].contents[1].contents[1].contents[3].getText()
        if "총합" in j:
            list_type.append("총합")
        elif "총액" in j:
            list_type.append("총액")
        elif "구글" in j:
            list_type.append("구글")
        elif "애플" in j:
            list_type.append("애플")
        else:
            continue
        temp=re.findall(r'\d+', j.replace(',', ''))[0] if len(re.findall(r'\d+', j.replace(',', ''))) !=0 else ""
        list_amount.append('' if temp=='' else int(temp))
        list_user.append(u[i].get("data-name")+"("+u[i].get("data-info")+")")
    print(p)

table=pd.DataFrame({"종류":list_type,"금액":list_amount,"닉네임":list_user})
table=table.drop_duplicates(["닉네임"])
title=list_user[0]+"~"+list_user[-1]+".xlsx"
print(title)
table.to_excel(title,index=False)