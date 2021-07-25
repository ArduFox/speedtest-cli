import speedtest

servers = []
# If you want to test against a specific server
# servers = [1234]

threads = None
# If you want to use a single threaded test
# threads = 1

print("---------------------------------------------")
print("deb_speed debugging speedtest inside cron job")
print("---------------------------------------------\n")

s = speedtest.Speedtest()
s.get_servers(servers)

print("\nServer dict with " +str(len(s.servers)) + " entries" )
if (len(s.servers)> 0):
    k = list(s.servers.keys())
    #print(k[0])
    print("first entry:\n" +str(s.servers[k[0]]))
    print("\nlast entry:\n"+ str(s.servers[k[-1]]))

    s.get_closest_servers()

    print("\n\nclosest Servers list with " + str(len(s.closest)) + " entries" )
    if (len(s.closest)> 0) :
        print("first entry:\n"+ str(s.closest[0]))
        print("\n last entry:\n"+ str(s.closest[-1]))

        s.get_best_server()

        print("\n\nbest Servers dict with " + str(len(s.best)) + " attributes" )
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







