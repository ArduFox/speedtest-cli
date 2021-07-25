import speedtest
import datetime
import time

servers = []
# If you want to test against a specific server
# servers = [1234]

threads = None
# If you want to use a single threaded test
# threads = 1

print("---------------------------------------------")
print("deb_speed debugging speedtest inside cron job")
print(datetime.datetime.now().strftime('%d.%m.%y %H:%M KW %V'))
print("---------------------------------------------\n")

s = speedtest.Speedtest()
condition = True

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
        time.sleep(6)      # sleep for 6 seconds
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

print("done.\n")







