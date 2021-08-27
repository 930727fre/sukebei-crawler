import eel,requests,csv
from lxml import html
from bs4 import BeautifulSoup
from os import mkdir,startfile,path,getcwd
from datetime import datetime

eel.init("web")
@eel.expose
def main(keyword,request_date,quantity,category,torrent_or_magnet):
    eel.show_percentage(0)
    quantity=int(quantity)
    if(quantity>500):
        quantity=500
    if(not path.exists(getcwd()+"\\downloads")):
        mkdir(getcwd()+"\\downloads")
    if(torrent_or_magnet=="1"):
        download_path=getcwd()+"\\downloads\\"+datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        eel.show_output("download path is "+path.abspath(download_path)+"\n")
        mkdir(download_path)
    with open('history.csv', 'a+',newline='',encoding="utf-8-sig") as file:#create the file if it's doesn't exist
        temp=1#with open have to do something
    with open('history.csv', 'r',newline='',encoding="utf-8-sig") as file:
        history_list = list(csv.reader(file))
    if(not len(history_list)==0):
        current_list=history_list
        row_of_keyword=-1
        for temp in range(len(history_list)):
            if(keyword==history_list[temp][0]):
                row_of_keyword=temp
                break
            elif(history_list[temp][0]=='' and len(history_list[temp])==0):#if user close the program while running ,that row would be empty and result in encode error
                history_list[temp][0]="error"
        if(row_of_keyword==-1):
            current_list.append([keyword])
            row_of_keyword=temp+1
    else:
        current_list=[[keyword]]
        row_of_keyword=0
        
    if category=="1":
        category="all categories"
    elif category=="2":
        category="Real Life - Videos"
    elif category=="3":
        category="Art - Anime"
    elif category=="4":
        category="Art - Manga"
    elif category=="5":
        category="Art - Pictures"
    elif category=="6":
        category="Art - Doujinshi"

    finished_times=0
    tempb=0
    for page in range(1,1000,1):
        url="https://sukebei.nyaa.si/"
        if keyword !="":
            url=url+"?f=0&c=0_0&q="+keyword+"&s=seeders&o=desc"
        else:
            url=url+"?s=seeders&o=desc"
        url+="&p="+str(page)
        
        try:
            web=requests.get(url)
        except:
            eel.show_output("fail to gain access to internet\n")
            return 0
        soup = BeautifulSoup(web.text, "lxml")
        
        temp=0
        while((not web.status_code==requests.codes.ok) and temp<20):
            web=requests.get(url)
            soup = BeautifulSoup(web.text, "lxml")
            temp+=1
            #print("reloading "+url+" "+str(temp))

        if(temp==20): #if tried 20 times without success then reutrn 0 or there is no page anymore
            eel.show_output("the site has shut down,i can only find "+str(finished_times)+",still "+str(quantity-finished_times)+" left.\n")
            #print("end")
            for temp in range(len(current_list)):
                if(current_list[temp][0]=='' and len(current_list[temp])==0):
                    current_list[temp][0]="error"#fill the bug row
            with open('history.csv', 'w',newline='',encoding="utf-8-sig") as file:
                csv.writer(file).writerows(current_list)
            if(torrent_or_magnet=="1"):
                    startfile(download_path)
            return 0
    
        
        eel.show_output("url="+url+"\n")
        for tr in soup.findAll(True, {"class":["success", "default","danger"]}):
            if(category==tr.select("a")[0].get("title") or category=="all categories"):
                if(request_date in tr.select("td")[4].string or len(request_date)==0):
                    if(tr.select("td")[3].string != "0 Bytes"):
                        if(not tr.select("td")[2].select("a")[1].get("href") in current_list[row_of_keyword]):
                            temp=((finished_times+1)/quantity*100)
                            eel.show_percentage(str('%.2f'%temp))
                            try:
                                if("comments" in tr.select("a")[1].get("class")): #if it doesn't have a class ,this error would be triggered
                                    temp=tr.select("a")[2].get("title")
                            except:
                                temp=tr.select("a")[1].get("title")
                            if(torrent_or_magnet=="1"):
                                temp=temp[0:246:1]#maximum length of file name in win10
                                for tempa in range(len(temp)):
                                    if(temp[tempa] in '\/:*?"<>|'):#special word that can't be named the name of a file in win10
                                        temp=temp.replace(temp[tempa]," ")
                                r = requests.get("https://sukebei.nyaa.si/"+tr.select("td")[2].select("a")[0].get("href"), allow_redirects=True)
                                filename=temp+".torrent"
                                while(not r.status_code==requests.codes.ok):
                                    r = requests.get("https://sukebei.nyaa.si/"+tr.select("td")[2].select("a")[0].get("href"), allow_redirects=True)
                                try:
                                    open(download_path+"\\"+filename, 'wb').write(r.content)
                                except:
                                    print("encoding triggered")
                                    print(finished_times+" "+filename)
                                    open(download_path+"\\"+filename, 'wb',encoding="utf-8-sig").write(r.content)
                            elif(torrent_or_magnet=="2"):
                                startfile(tr.select("td")[2].select("a")[1].get("href"))
                            eel.show_output((str(finished_times+1)+"."+temp+"\n"))
                            finished_times+=1
                            current_list[row_of_keyword].append(tr.select("td")[2].select("a")[1].get("href"))
                                    
            if(finished_times>=quantity):
                #print("end")
                eel.show_output("mission complete\n")
                for temp in range(len(current_list)):
                    if(current_list[temp][0]=='' and len(current_list[temp])==0):
                        current_list[temp][0]="error"#fill the bug row
                with open('history.csv', 'w',newline='',encoding='utf-8-sig') as file:
                    csv.writer(file).writerows(current_list)
                if(torrent_or_magnet=="1"):
                    startfile(download_path)
                return 0
        #print("in page"+str(page)+" find "+str((finished_times-tempb)))
        tempb=finished_times
#pyinstaller commend :pyinstaller --add-data="web\main.html;." --add-data="web\main.js;." --onedir main.py


eel.start('main.html',size = (620,620))

