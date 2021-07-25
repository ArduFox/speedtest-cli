import speedtest
import datetime
#from datetime import timedelta
import time


servers = []
# If you want to test against a specific server
# servers = [1234]

threads = None
# If you want to use a single threaded test
# threads = 1

s = speedtest.Speedtest()
condition = True
pause = 21

print("---------------------------------------------")
print("deb_speed debugging speedtest inside cron job")
print(datetime.datetime.now().strftime('%d.%m.%y %H:%M KW %V'))
print("---------------------------------------------\n")


loops=0
while condition:
    loops= loops+1
    s.get_servers(servers)

    condition = (loops < 5) and (len(s.servers) == 0)

    print(str(loops)+": server dict with " +str(len(s.servers)) + " entries" )

    if (len(s.servers)== 0):
        time.sleep(pause*loops)      # sleep for 6 seconds
    else:
        k = list(s.servers.keys())
        #print("first entry:\n" +str(s.servers[k[0]]))
        #print("\nlast entry:\n{s.servers[k[-1]]})

        s.get_closest_servers()

        print("\nclosest Servers list with " + str(len(s.closest)) + " entries" )
        print("-------------------------------------")
        if (len(s.closest)> 0) :
            print("first entry:\n"+ str(s.closest[0]))
            print("\nlast entry:\n"+ str(s.closest[-1]))

            s.get_best_server()

            print("\n\nbest Servers dict with " + str(len(s.best)) + " attributes" )
            print("-----------------------------------------")
            if (len(s.best)> 0):
                print(s.best)

                s.download(threads=threads)
                s.upload(threads=threads)
                s.results.share()

                print("\n-----------------")
                print(  "results from test")
                print(  "-----------------")

                print (s.results.dict())

print("done scanning, writing csv.\n")

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


csv_str=""
csv_header=""
for k in csv_row.keys():
    csv_header = csv_header + '"'+ k + '"; '
    
csv_header=csv_header[:-2]+"\n"

for k in csv_row.keys():
    value=csv_row[k]
    
    #print(k, value, type(value))
        
    # https://stackoverflow.com/questions/35490420/how-to-check-type-of-object-in-python
    if (isinstance(value, float)) or (isinstance(value, int)):
        csv_str = csv_str + str(value) + "; "
    else:
        csv_str = csv_str + '"'+ str(value) + '"; '
csv_str=csv_str[:-2] + "\n"


if True:
    with open('deb_speed.csv', 'w', encoding='utf-8') as f:
        f.write(csv_header)
        f.write(csv_str)
else:   
    with open('deb_speed.csv', 'a', encoding='utf-8') as f:
        f.write(csv_str)
    

print("done.\n")




