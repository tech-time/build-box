import os, sys
import configparser

#Buildbox configuration class
class BuildboxParameter:

        
        def __init__(self, path):
                self.parameters = dict()
                self.pathToConfigurationFile = path
                self.configParser = configparser.ConfigParser()


        #Add a new parameter or update the parameter
        def addParam(self, paramName, value):
                if(self.parameters.has_key(paramName)):
                        self.parameters[paramName] = value
                else:
                        self.parameters.append(paramName, value)


        #Return the value associated to the parameter name or null if parameter does not exists
        def getParam(self, paramName):
                if(paramName in self.parameters):
                        return self.parameters[paramName]
                else:
                        return ''


        #Read configuration from ini file and add parameters
        def readConfigurationFromIniFile(self):
                self.configParser.read(self.pathToConfigurationFile)
                sections = self.configParser.sections()
                for section in sections:
                        options = self.configParser.options(section)
                        for option in options:
                                try:
                                        self.parameters[option] = self.configParser.get(section, option)
                                        if self.parameters[option] == -1:
                                                print("skip: %s" % option)
                                except:
                                        print("exception on %s" % option)
                                        self.parameters[option] = None
                print(self.parameters) 


#Main
buildbox = BuildboxParameter("pathToConfigurationFile")
buildbox.readConfigurationFromIniFile()
print(buildbox.getParam('parameter_name'))
print(buildbox.getParam('parameter_name'))
