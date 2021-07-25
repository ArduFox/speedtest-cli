# Problems using speedtest as cron job on Raspberry

I am using speedtest (`speedtest-cli==2.1.4b1`) as python library and also speedtest-cli to monitor me internet provider on a raspberry2 and 3. 

If I start my jobs as standard user or as root everything works as intended. But if I start my jobs as cronjobs, 
they exit with `ERROR: Unable to connect to servers to test latency`

And yes my aother cronjobs work as intended and i don't think am doing cron the wrong way.


## :star: it works :star:
- code is up and running
- appends to hard coded csv file with local path :-(
- testing if it works for some hours   


## to do :hammer:

1. Work on test code an monitor the results and improve this code to become more robust
1. Save the results to my .csv data collection. 

## debug and prepare to fork :construction:

- line 1440 in `/usr/local/lib/python2.7/dist-packages/speedtest.py` calls function `get_best_server(self, servers=None)`
  - if first entry in list of dict (key=latency, val = servername) ist None / empty after sorting the servers by latency then raise error
      - if servers in call are None, then call `self.get_closest_servers()` 
  - call to `get_best_server` is at line 1938 `speedtest.get_best_server()` without params as long there is no mini server in arguments
      - is the serverlist inside cron empty?
      - servers will be collected by `speedtest.get_servers()`  (def at line 1240) by reading xml from `https://www.speedtest.net/speedtest-servers-static.php` et al.
    
## ideas :bulb:

- test debugging code on PC in Jupyter that:
  -  uses the lib and checks step by step content of servers at all, closest servers, best servers
- transport this code to both Raspis and into this fork
- testing inside and outside cron

### first results

- from time to time speedtest doesn't find the initial list of servers
  1. retry this early stage for some times with maybe increasing waiting times
  1. have a standard list of closest servers as fall back. Maybe after each succesfull attempt save them to a file.


## internet ressources

- https://askubuntu.com/questions/1322451/speedtest-cli-does-not-execute-when-scheduled-cron
- https://askubuntu.com/questions/1332969/problem-with-speedtest-cli sugests to alter the code 😳 but is already outdated. snippet at line 1501:
``` py
      try:
            fastest = sorted(results.keys())[0]
        except IndexError:
            raise SpeedtestBestServerFailure('Unable to connect to servers to '
                                             'test latency.')

```
