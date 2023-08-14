import requests
import time
import json

apikey="APIKEY" #Must be a string
profiles = ["PROFILE1","PROFILE2","..."] # Must be a list; one or more profiles
fetch_interval = 60 # The interval the script will pull data from the API (if you use crontab ensure its in sync with your cron planning e.g. script runtime every minute = 60 seconds in that variable)
crontab_mode = 1 #1 if you want to run this script in crontab; 0 if the script should run endless
write_file = 0 # 1=yes #no print output 0=no #print output
tmp_file_path = "/tmp/" # Only used if write_file = 1 > Here are temporary files written which are non persistent (e.g. after reboot)
log_file_path = "/var/log/" # Only used if write_file = 1 > Here are log files written which are persistent (e.g. after reboot)

def make_request(url,headers):
    global write_file
    global tmp_file_path
    global log_file_path
    #print(url) #Debugging
    headers = headers
    response = requests.get(url, headers=headers)
    response_code = response.status_code
    response = response.content
    response = response.decode()
    if '"data":[]' in response:
        None
    else:
        parsed_json = json.loads(response)
        json_data = parsed_json.get("data")
        json_meta = parsed_json.get("meta")
        try:
            for content in json_data:
                get_device = content.get("device")
                content["meta"] = json_meta
                for add_device_info in get_device:
                    content["device_"+add_device_info] = get_device[add_device_info]
                content = json.dumps(content)
                if write_file == 1:
                    file_writer(tmp_file_path+"nextdns_log_streamer.json","a",content,"y")
                else:
                    print(content)
        except:
            None
    return response_code

def get_unixtime(lenght):
    unixtime = time.time()
    unixtime = unixtime - fetch_interval
    unixtime = str(unixtime)[:lenght]
    return unixtime

def file_writer(f_path,f_mode,f_content,f_newline="n"):
    f = open(f_path, f_mode)
    if f_newline == "n":
        f.write(f_content)
    else:
        f.write(f_content+"\n")
    f.close()

def execute(fetch_interval,starttime):
    global waserror
    global error_time
    global startover
    #print(starttime) #Debugging
    for profile in profiles:
        if waserror == 0:
            response_code = make_request("https://api.nextdns.io/profiles/"+profile+"/logs?from="+starttime,{"X-Api-Key": apikey})
            if response_code == 200:
                file_writer(log_file_path+"nextdns_log_streamer_time.log","w",starttime)
            else:
                waserror = 1
                error_time = starttime
                file_writer(log_file_path+"nextdns_log_streamer_time.log","w",error_time)
    if crontab_mode == 0:
        if waserror == 0:
            current_time = get_unixtime(10)
            allowed_time = int(current_time) - int(fetch_interval)
            if (int(starttime) >= int(allowed_time)) or startover == 1:
                time.sleep(fetch_interval)
                new_starttime = str(int(starttime) + int(fetch_interval))
                execute(fetch_interval,new_starttime)
            else:
                waserror = 0
                startover = 1
                #print ("Starting over")
                execute(fetch_interval,current_time)    
        else:
            waserror = 0
            time.sleep(fetch_interval)
            execute(fetch_interval,error_time)
#Run Script
error_time = ""
read_time = ""
waserror = 0
startover = 0

#Check error time or last runtime
try:
    f = open(log_file_path+"nextdns_log_streamer_time.log", "r")
    read_time= str(f.read()).replace("\n","")
    f.close()
    try:
        f = open(tmp_file_path+"nextdns_log_streamer_startover.log", "r")
        read_startover= str(f.read()).replace("\n","")
        f.close()
    except:
        read_startover = "0"
except:
    None

#Check if valid UNIX Timestamp
if "1" in read_time or "2" in read_time or "3" in read_time or "4" in read_time or "5" in read_time or "6" in read_time or "7" in read_time or "8" in read_time or "9" in read_time:
    if crontab_mode == 0:
        execute(fetch_interval,read_time)
    if crontab_mode == 1 and read_startover == "0":
        execute(fetch_interval,read_time)
        file_writer(tmp_file_path+"nextdns_log_streamer_startover.log","w","1")
    if crontab_mode == 1 and read_startover == "1":
        init_starttime = get_unixtime(10)
        execute(fetch_interval,init_starttime)
else:
    init_starttime = get_unixtime(10)
    execute(fetch_interval,init_starttime)
