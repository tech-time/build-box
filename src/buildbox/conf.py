import configparser


# Buildbox configuration class
class BuildboxParameter:
    def __init__(self, path):
        self.parameters = dict()
        self.pathToConfigurationFile = path
        self.configParser = configparser.ConfigParser()

    # Add a new parameter or update the parameter
    def addParam(self, paramName, value):
        if (self.parameters.has_key(paramName)):
            self.parameters[paramName] = value
        else:
            self.parameters.append(paramName, value)

    # Return the value associated to the parameter name or null if parameter does not exists
    def getParam(self, paramName):
        if (paramName in self.parameters):
            return self.parameters[paramName]
        else:
            return ''

    # Return the int value associated to the parameter name or a given default value if parameter does not exist
    def getIntParam(self, paramName, defaultValue = None):
        v = self.getParam(paramName)
        if v == "": # if not found or empty : returns the default value
            return defaultValue
        else:
            return int(v)

    # Read configuration from ini file and add parameters
    def readConfigurationFromIniFile(self):
        self.configParser.read(self.pathToConfigurationFile)
        for section in self.configParser.sections():
            for option in self.configParser.options(section):
                try:
                    self.parameters[option] = self.configParser.get(section, option)
                    if self.parameters[option] == -1:
                        print("skip: %s" % option)
                except:
                    print("exception on %s" % option)
                    self.parameters[option] = None
                    # print(self.parameters)

# Main
