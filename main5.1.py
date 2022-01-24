import requests,csv,subprocess,time,platform
from bs4 import BeautifulSoup
from os import mkdir,path,getcwd,startfile
from datetime import datetime
from tqdm import tqdm
from configuration import *



operating_system=platform.system()

def main():
    global keyword,quantity,category,torrent_or_magnet
    
    if(quantity>500):
        quantity=500
    if(not path.exists("downloads")):
        mkdir("./downloads")
    if(torrent_or_magnet=="1"):
        download_path=getcwd()+"/downloads/"+datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
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
        if(operating_system=="Windows"):
            #startfile(download_path)
            pass
        elif(operating_system=="Linux"):    
            subprocess.call(["xdg-open", download_path])#xdg-open is only supported in few distros, e.g. Ubuntu.
    
    pbar=tqdm(total=quantity,bar_format="{n_fmt}/{total_fmt}{bar}|{percentage:3.0f}%|:{desc}")
    
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
            print("Fail to gain access to sukebei.nayy.si.\n")
            return 0
        soup = BeautifulSoup(web.text, "lxml")
        #print(url)
        temp=0 #times trying to request the url
        while((not web.status_code==requests.codes.ok) and temp<20):
            web=requests.get(url)
            soup = BeautifulSoup(web.text, "lxml")
            time.sleep(2)
            temp+=1
            #print("reloading "+url+" "+str(temp))
        if(temp==20): #if web.status shows something wrong over 20 attempts, then end the process.
            print("The site is accessible, but there are some problewms with the nyaa itself.")
            print("Web status:"+str(web.status_code))
            print("Finished requests:"+str(finished_times)+",and "+str(quantity-finished_times)+" remain undone.\n")
            
            for temp in range(len(current_list)):
                if(current_list[temp][0]=='' and len(current_list[temp])==0):
                    current_list[temp][0]="error"#fill the bug row
            with open('history.csv', 'w',newline='',encoding="utf-8-sig") as file:
                csv.writer(file).writerows(current_list)
            print("Process ends.")
            return 0
        
        #print("url="+url+"\n")
        for tr in soup.findAll(True, {"class":["success", "default","danger"]}):
            if(category==tr.select("a")[0].get("title") or category=="all categories"):
                if(tr.select("td")[3].string != "0 Bytes"):
                    try:
                        if("comments" in tr.select("a")[1].get("class")): #if there isn't a class, this error would be triggered
                            filename=tr.select("a")[2].get("title")
                    except:
                        filename=tr.select("a")[1].get("title")
                    if(not filename in current_list[row_of_keyword]):
                        if(torrent_or_magnet=="1"):
                            for temp in range(len(filename)):
                                if(filename[temp] in '\/:*?"<>|'):#special word that should be excluded in Windows
                                    filename=filename.replace(filename[temp]," ")
                            r = requests.get("https://sukebei.nyaa.si/"+tr.select("td")[2].select("a")[0].get("href"), allow_redirects=True)
                            filename=bytes(filename, 'utf-8').decode('utf-8', 'ignore')
                            while(not r.status_code==requests.codes.ok):
                                time.sleep(2)
                                r = requests.get("https://sukebei.nyaa.si/"+tr.select("td")[2].select("a")[0].get("href"), allow_redirects=True)
                            pbar.set_description(filename)
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
                            if(operating_system=="Windows"):
                                startfile(tr.select("td")[2].select("a")[1].get("href"))
                            elif(operating_system=="Linux"):
                                subprocess.call(["xdg-open", tr.select("td")[2].select("a")[1].get("href")])
                        tempa=((finished_times+1)/quantity*100)
                        #print("Progress:"+str('%.2f'%tempa))
                        #print(str(finished_times+1)+"."+temp)
                        finished_times+=1
                        pbar.update(1)
                        current_list[row_of_keyword].append(temp)
                                    
            if(finished_times>=quantity):
                #print("mission complete")
                for temp in range(len(current_list)):
                    if(current_list[temp][0]=='' and len(current_list[temp])==0):
                        current_list[temp][0]="error"#fill the bug row
                with open('history.csv', 'w',newline='',encoding='utf-8-sig') as file:
                    csv.writer(file).writerows(current_list)
                #print("Process ends.")
                return 0
        #print("in page"+str(page)+" find "+str((finished_times-tempb)))
        tempb=finished_times

if(operating_system!="Windows" and operating_system!="Linux"):
    print("Your operating system is not supported.")
else:
    main()



