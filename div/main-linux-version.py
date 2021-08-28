import eel,requests,csv,subprocess,time
from lxml import html
from bs4 import BeautifulSoup
from os import mkdir,path,getcwd
from datetime import datetime

eel.init("web")
@eel.expose
def main(keyword,request_date,quantity,category,torrent_or_magnet):
    eel.show_percentage(0)
    quantity=int(quantity)
    if(quantity>500):
        quantity=500
    if(not path.exists("downloads")):
        mkdir("./downloads")
    if(torrent_or_magnet=="1"):
        download_path=getcwd()+"/downloads/"+datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        eel.show_output("Download path="+path.abspath(download_path)+"\n")
        mkdir(download_path)
    with open('history.csv', 'a+',newline='',encoding="utf-8-sig") as file:#create the file if it's doesn't exist
        temp=1
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
    if(torrent_or_magnet=="1"):
        subprocess.call(["xdg-open", download_path])
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
            eel.show_output("Fail to gain access to sukebei.nayy.si.\n")
            return 0
        soup = BeautifulSoup(web.text, "lxml")
        
        temp=0
        while((not web.status_code==requests.codes.ok) and temp<20):
            web=requests.get(url)
            soup = BeautifulSoup(web.text, "lxml")
            time.sleep(2)
            temp+=1
            #print("reloading "+url+" "+str(temp))
        if(temp==20): #if tried 20 times without success, then reutrn 0 or there is no page anymore
            eel.show_output("the site has been shut down,I can only find "+str(finished_times)+",still "+str(quantity-finished_times)+" left.\n")
            #print("end")
            for temp in range(len(current_list)):
                if(current_list[temp][0]=='' and len(current_list[temp])==0):
                    current_list[temp][0]="error"#fill the bug row
            with open('history.csv', 'w',newline='',encoding="utf-8-sig") as file:
                csv.writer(file).writerows(current_list)
            return 0

        
        eel.show_output("url="+url+"\n")
        for tr in soup.findAll(True, {"class":["success", "default","danger"]}):
            if(category==tr.select("a")[0].get("title") or category=="all categories"):
                if(request_date in tr.select("td")[4].string or len(request_date)==0):
                    if(tr.select("td")[3].string != "0 Bytes"):
                        try:
                            if("comments" in tr.select("a")[1].get("class")): #if it doesn't have a class ,this error would be triggered
                                filename=tr.select("a")[2].get("title")
                        except:
                                filename=tr.select("a")[1].get("title")      
                        if(not filename in current_list[row_of_keyword]):
                            if(torrent_or_magnet=="1"):
                                for temp in range(len(filename)):
                                    if(filename[temp] in '\/:*?"<>|'):#special word that can't be named the name of a file in win10
                                        filename=filename.replace(filename[temp]," ")
                                r = requests.get("https://sukebei.nyaa.si/"+tr.select("td")[2].select("a")[0].get("href"), allow_redirects=True)
                                filename=bytes(filename, 'utf-8').decode('utf-8', 'ignore')
                                while(not r.status_code==requests.codes.ok):
                                    time.sleep(2)
                                    r = requests.get("https://sukebei.nyaa.si/"+tr.select("td")[2].select("a")[0].get("href"), allow_redirects=True)
                                temp=filename
                                filename=download_path+"/"+filename
                                tempa=0#bytes
                                tempb=0#sum of bytes
                                while(True):
                                    if(tempb>=245):
                                        filename=filename[0:tempa-1:1]
                                        break
                                    elif(tempa==len(filename)-1):
                                        break
                                    tempb=tempb+len(filename[tempa].encode('utf-8'))
                                    tempa=tempa+1

                                open(filename+".torrent", 'wb').write(r.content)
                            elif(torrent_or_magnet=="2"):
                                subprocess.call(["xdg-open", tr.select("td")[2].select("a")[1].get("href")])
                            tempa=((finished_times+1)/quantity*100)
                            eel.show_percentage(str('%.2f'%tempa))                           
                            eel.show_output((str(finished_times+1)+"."+temp+"\n"))
                            finished_times+=1
                            current_list[row_of_keyword].append(temp)
                                    
            if(finished_times>=quantity):
                #print("end")
                eel.show_output("mission complete\n")
                for temp in range(len(current_list)):
                    if(current_list[temp][0]=='' and len(current_list[temp])==0):
                        current_list[temp][0]="error"#fill the bug row
                with open('history.csv', 'w',newline='',encoding='utf-8-sig') as file:
                    csv.writer(file).writerows(current_list)
                return 0
        #print("in page"+str(page)+" find "+str((finished_times-tempb)))
        tempb=finished_times
#pyinstaller commend :pyinstaller --add-data="web\main.html;." --add-data="web\main.js;." --onedir main.py


eel.start('main.html',size = (620,620))

