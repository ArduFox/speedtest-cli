####################################################
#                                                  #
#  speedtest4cron.py                               #
#                                                  #
#  sometimes, when run in cron speedtest           #
#  stops with error                                #
#                                                  #
#  this python script allows debugging and         #
#  retries the fetch the list of servers           #
#  on my system, that was the problem              #
#                                                  #
####################################################

import speedtest
import datetime
#from datetime import timedelta
import time


def do_speedtest(s,loops):
    s.download(threads=threads)
    s.upload(threads=threads)
    s.results.share()

    my_print("\n-----------------")
    my_print(  "results from test")
    my_print(  "-----------------")

    my_print (s.results.dict())



    my_print("done scanning, writing csv.\n")

    csv_row=dict()

    at=datetime.datetime.strptime(s.results.dict()['timestamp'],"%Y-%m-%dT%H:%M:%S.%fZ")  
    csv_row['query_time']=at.strftime("%Y-%m-%d %H:%M:%S")
    csv_row['ip']=s.results.dict()['client']['ip']
    csv_row['provider']=s.results.dict()['client']['isp']
    csv_row['provider_rating']=float(s.results.dict()['client']['isprating'])
    csv_row['speed_down']=round(s.results.dict()['download']/1024/1024,3)
    csv_row['speed_up']=round(s.results.dict()['upload']/1024/1024,3)
    csv_row['ping']=round(s.results.dict()['ping'],1)
    csv_row['response']=csv_row['ping']
    csv_row['distance']=round(s.results.dict()['server']['d'],1)
    csv_row['link_to_pic']=s.results.dict()['share']
    csv_row['host']=s.results.dict()['server']['host']
    csv_row['company']=s.results.dict()['server']['sponsor'] + ", " + s.results.dict()['server']['name']
    csv_row['server_id']=int(s.results.dict()['server']['id'])
    #csv_row["days_old"]=round((datetime.datetime.now() - at) / timedelta(days=1),1)
    csv_row["days_old"]=0       # data is from now an 0 days old :-)
    csv_row["week"]=int(at.strftime("%V") )
    csv_row["attempts"]=loops


    return csv_row

    
def write_header(csv_row, collist=None, filename='/home/pi/speed.csv'):
    csv_header=""
    
    if collist == None:
        for k in csv_row.keys():
            csv_header = csv_header +  k + ';'

    else:
        for c in collist:
            csv_header = csv_header +  c + ';'
            
    csv_header=csv_header[:-1]+"\n"
    
    with open(filename, 'w') as f:
        f.write(csv_header)
        
    return csv_header
    

def append_line(csv_row, collist=None, filename='/home/pi/speed.csv'):     
    csv_str=""

    if collist == None:
        for k in csv_row.keys():
            value=csv_row[k]
            csv_str = csv_str + str(value) + ";"
            
    else:
        for c in collist:
           csv_str = csv_str + str(csv_row[c]) + ";" 
        
    csv_str=csv_str[:-1] + "\n"        
    
    with open(filename, 'a') as f:
        f.write(csv_str)

    return csv_str


servers = []
# If you want to test against a specific server
# servers = [1234]

threads = None
# If you want to use a single threaded test
# threads = 1

s = speedtest.Speedtest()
condition = True
pause = 21

global_do_print=False

def my_print(*argv):
    if global_log:
        print(*argv)

my_print("---------------------------------------------")
my_print("deb_speed debugging speedtest inside cron job")
my_print(datetime.datetime.now().strftime('%d.%m.%y %H:%M KW %V'))
my_print("---------------------------------------------\n")

cols=['query_time', 'speed_down', 'speed_up', 'ping', 'response', 
      'link_to_pic','distance', 'host', 'company', 'server_id', 
      'ip', 'attempts', 'provider', 'provider_rating',
      'days_old', 'week']


loops=0
while condition:
    loops= loops+1
    s.get_servers(servers)

    condition = (loops < 5) and (len(s.servers) == 0)
    
    my_print(str(loops)+": server dict with " +str(len(s.servers)) + " entries" )

    if (len(s.servers)== 0):
        time.sleep(pause*loops)  # sleep 
    else:

        k = list(s.servers.keys())
        #print("first entry:\n" +str(s.servers[k[0]]))
        #print("\nlast entry:\n{s.servers[k[-1]]})

        s.get_closest_servers()

        my_print("\nclosest Servers list with " + str(len(s.closest)) + " entries" )
        my_print("-------------------------------------")
        if (len(s.closest)> 0) :
            my_print("first entry:\n"+ str(s.closest[0]))
            my_print("\nlast entry:\n"+ str(s.closest[-1]))

            s.get_best_server()

            my_print("\n\nbest Servers dict with " + str(len(s.best)) + " attributes" )
            my_print("-----------------------------------------")
            if (len(s.best)> 0):
                csv=do_speedtest(s,loops)
                line=write_header(csv,collist=cols,filename='/home/pi/speed.csv')
                line=append_line(csv,collist=cols,filename='/home/pi/speed.csv')
