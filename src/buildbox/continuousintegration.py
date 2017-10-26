'''
Build interface
 - initialise interface with Build server (Jenkins)
 - interface with build server to get build results


 Build results contain:
  - A status indicator (from 0 to 100)
  - A health indicator (sunny or cloudy)
  - a project name


  TODO : import jenkinsapi, connect to the server, read a list of builds from config file and translate job results
'''

from threading import Thread


class Jobs(Thread):
    _index = 0
    _builds = None

    def __init__(self):
        self._builds = [Builditem(15, 50, "job1"),
                        Builditem(30, 10, "job2"),
                        Builditem(25, 90, "job3"),
                        Builditem(75, 99, "job4"),
                        Builditem(95, 75, "job5")]
        self._index=0
        pass

    def getnextbuild(self):
        b = self._builds[self._index]
        self._index = (self._index + 1) % len(self._builds)
        return b


    def run(self):
        # Do something like poll jbuild server ,...
        self._top.mainloop()



class Builditem():
    status = 0
    health = 0
    name = ""
    def __init__(self, s, h, n):
        self.status=s
        self.health=h
        self.name=n

