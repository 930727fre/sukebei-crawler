import requests,csv,subprocess,time,platform,sys
from bs4 import BeautifulSoup
from os import mkdir,path,getcwd,walk,rmdir
from datetime import datetime
from tqdm import tqdm
from configuration import *


operating_system=platform.system()
bt_list=[]
filename_list=[]


print("Configuration:")
if(keyword=="blank"):
    print("Keyword: None")
else:
    print("Keyword: " + keyword)
print("Requests quantity: " + str(quantity))
print("Category: " + category)
print("Torrent or magnet: " + str(torrent_or_magnet))
print()
input("Press any key to continue...")

if keyword=="":
    keyword="blank"

if(operating_system=="Windows"):
    from os import startfile #Since there is no startfile() in Linux version's library

def main():
    global keyword,quantity,category,torrent_or_magnet
    
    if(not path.exists("Downloads")):
        mkdir("./Downloads")
    if(torrent_or_magnet=="1"):
        download_path=getcwd()+"/Downloads/"+datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        mkdir(download_path)
    with open('db.csv', 'a+',newline='',encoding="utf-8-sig") as file:#create the file if it's doesn't exist
        temp=1
    with open('db.csv', 'r',newline='',encoding="utf-8-sig") as file:
        db = list(csv.reader(file))
    
    if(db==[]):
        print("all new db.csv")
        db=[["keyword",]]
    if(not len(db[0])==0):
        row_of_keyword = -1
        for temp in range(len(db)):
            if(keyword == db[temp][0]):
                row_of_keyword = temp
                break
        if(row_of_keyword == -1):
            db.append([keyword])
            row_of_keyword = temp+1
    else:
        db = [[keyword]]
        row_of_keyword = 0
        
    if category == "1":
        category = "all categories"
    elif category == "2":
        category = "Real Life - Videos"
    elif category == "3":
        category = "Art - Anime"
    elif category == "4":
        category = "Art - Manga"
    elif category == "5":
        category = "Art - Pictures"
    elif category == "6":
        category = "Art - Doujinshi"

    finished_times = 0
    tempb = 0
    if(torrent_or_magnet == "1"):
        if(operating_system == "Windows"):
            startfile(download_path)
        elif(operating_system=="Linux"):    
            try:
                subprocess.call(["xdg-open", download_path])#xdg-open is only supported in few distros, e.g. Ubuntu.
            else:
                print("xdg-open is not available")
    
    print("status: crawling")
    page=1
    while(True):
        url="https://sukebei.nyaa.si"
        if keyword =="blank":
            url=url+"/?s=seeders&o=desc"
        else:
            url=url+"/?f=0&c=0_0&q="+keyword+"&s=seeders&o=desc"
        url+="&p="+str(page)
        print("url:"+url)
        
        try:
            web=requests.get(url)
        except:
            print("Fail to gain access to sukebei.nayy.si.\n")
            return
        soup = BeautifulSoup(web.text, "lxml")
        temp=0 #times trying to request the url
        while((not web.status_code==requests.codes.ok) and temp<5):
            web=requests.get(url)
            soup = BeautifulSoup(web.text, "lxml")
            time.sleep(2)
            temp+=1
            print("reloading "+url+" "+str(temp))
        if(temp==5): #if web.status shows something wrong over 20 attempts, then end the process.
            print("The site is accessible, but there are some problewms with the nyaa itself.")
            print("Web status:"+str(web.status_code))
            print("Finished requests:"+str(finished_times)+",and "+str(quantity-finished_times)+" remain undone.\n")
            
            with open('db.csv', 'w',newline='',encoding="utf-8-sig") as file:
                csv.writer(file).writerows(db)
            print("Process ends.")
            return 0


        for tr in soup.findAll(True, {"class":["success", "default","danger"]}):
            if(category==tr.select("a")[0].get("title") or category=="all categories"):
                if(tr.select("td")[3].string != "0 byte"):
                    try:
                        if("comments" in tr.select("a")[1].get("class")): #if there isn't a class, this error would be triggered
                            filename=tr.select("a")[2].get("title")
                    except:
                        filename=tr.select("a")[1].get("title")
                    if(not filename in db[row_of_keyword]):
                        if(torrent_or_magnet=="1"):
                            bt_list.append("https://sukebei.nyaa.si/"+tr.select("td")[2].select("a")[0].get("href"))
                            filename_list.append(filename)

                        
                        finished_times+=1
                        db[row_of_keyword].append(filename)

            if(finished_times==quantity):
                break
        
        tempb=finished_times
        if soup.find_all("li", {"class":"next disabled"}) or finished_times==quantity:
            break
        page=page+1
    print("status: crwaling finished.")
    print("status: downloading")
    if torrent_or_magnet=="1":
        for i in tqdm(range(len(bt_list))):
            filename=filename_list[i]
            for temp in range(len(filename)):
                if(filename[temp] in '\/:*?"<>|'):#special word that should be excluded in Windows
                    filename=filename.replace(filename[temp]," ")
            r = requests.get(bt_list[i], allow_redirects=True)
            filename=bytes(filename, 'utf-8').decode('utf-8', 'ignore') #remove unsupported character in utf-8
            temp=1
            while(not r.status_code==requests.codes.ok):
                time.sleep(2)
                r = requests.get(bt_list[i], allow_redirects=True)
                temp=temp+1
                if temp==5:
                    break
            filename=download_path+"/"+filename
            """
            while(True):
                if(sys.getsizeof(filename)>=254):
                    filename=filename[:-1]
                else:
                    break
            """
            open(filename+".torrent", 'wb').write(r.content)
    elif(torrent_or_magnet=="2"):
        for i in range(len(bt_list)):
            if(operating_system=="Windows"):
                startfile(bt_list[i])
            elif(operating_system=="Linux"):
                subprocess.call(["xdg-open", bt_list[i]])
    db[row_of_keyword]=db[row_of_keyword]+filename_list
    with open('db.csv', 'w',newline='',encoding='utf-8-sig') as file:
        csv.writer(file).writerows(db)
    print("Process finished.")


    

if(operating_system!="Windows" and operating_system!="Linux"):
    print("Your operating system is not supported.")
else:
    main()
    
    root = './Downloads'
    folders = list(walk(root))[1:]

    for folder in folders:
        if not folder[2]:
            rmdir(folder[0])




