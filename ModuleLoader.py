import imp
import os

ModuleFolder = "./modules"
MainModule = "Start"


def getModules():
    modules = []
    possibleModules = os.listdir(ModuleFolder)
    for i in possibleModules:
        location = os.path.join(ModuleFolder, i)
        if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
            continue
        info = imp.find_module(MainModule, [location])
        modules.append({"name": i, "info": info})
    return modules


def loadModule(module):
    return imp.load_module(MainModule, *module['info'])