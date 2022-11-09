
import sys
import configparser

class ychat_config:
    def __init__(self,fconfig) -> None:
        self.fconfig=fconfig
        hconfig = configparser.ConfigParser()
        hconfig.sections()
        hconfig.read(fconfig)

        self.hconfig=hconfig

    def getconfig(self):
        return(self.hconfig)
    


