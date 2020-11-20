import os
from urllib.parse import urlparse
import json
from mpm_tools.Global import Global 
from mpm_tools.SystemManager import SystemManager 
from mpm_tools.NetworkManager import NetworkManager 
from mpm_tools.FileManager import FileManager 
from mpm_tools.Tools import Tools
from progress.bar import Bar
from pathlib import Path
#from tools.Responder import Responder 

netMan = NetworkManager()
fileMan = FileManager()
gb = Global()
sysMan = SystemManager()
tools = Tools()
res = gb.getFundInfos("responses")
separator = "/"
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="mpm your full command line")
    #parser.add_argument("cmd", type=str, metavar="create", help="Specify a command you want to execute")
    
    
    
    parser.add_argument("-u", "--update",required=False, help="update your local mpm database")
    parser.add_argument("-b", "--bored",required=False, help="uninstall mpm")
    parser.add_argument("-d" , help="Specify the name of the directory you want to store the output of the command")
    parser.add_argument("-v", "--version",required=False, help="see the installed version of mpm")
    group = parser.add_mutually_exclusive_group()

    
    group.add_argument("-c", "--create", help="create a complete project from the templates in our repositories")
    group.add_argument("-i", "--install", help="install a plugin or a module")

    group.add_argument("-o", "--clone", help="clone any zip file just using his url")
    group.add_argument("-f", "--fileload", help="download any file and put it in the current directory just using his url")
    
    
    #parser.add_argument("-up", "--upgrade",required=False, help="upgrade globally mpm and get the newest version")
    

    args = parser.parse_args()

    
    myOs = gb.getFundInfos("os")

    if args.create or args.install or args.clone:
        db = netMan.readFileFromUrl(gb.getFundInfos("url"))
        if not isinstance(db, bool):
            try:      
                fileMan.getSourceDir().createFile("package.mgx")
                packages = fileMan.getSourceDir().getFileContent("package.mgx", "")
                packages = {"projects": "", "modules": "", "cloned":"", "version": gb.getFundInfos("version")} if str(packages)=="" else json.loads(packages) 
            except Exception as e:
                print("Something went wrong. Try to delete the packages.mgx file")
                exit()
        else:
            print("problem to contact our database")
            exit()
            """
            errorContent = str(e)
            errorSup = fileMan.setSrcDir().getFileContent("/error.log")
            if not errorSup:
                errorContent+=errorSup
            fileMan.delFile("error.log")
            fileMan.getSourceDir().createFile("error.log", e)
            print(e)
            """
            exit()
    
    

    if args.create:
        currentArg = args.create
        """
        if args.create in packages["projects"]:
            print(args.create, " already installed")
            print(packages)
            exit()
        """    
        if db:
            db = json.loads(db)
            try:
                found = tools.in_json_array(currentArg, "name", db["projects"])
            except Exception as e:
                print("Something went wrong : problem to contact the database")
                exit()

            

            if(found[0]):
                req = db["projects"][found[1]]
                directory = currentArg if not args.d else args.d
                print("creating of", currentArg, " project")
                if req["git"]!="":
                    print("downloading and installing")
                    if netMan.gitClone(req["git"], directory):
                        print(res["process_completed"])
                        print("\n")
                        print("project created in the following directory :", directory)
                        packages["projects"]+=currentArg
                        packages["projects"]+=" "
                        with open(fileMan.getSourceDir().getCurrentSrcDir()+separator+'package.mgx', 'w') as outfile:
                            json.dump(packages, outfile)

                        fileMan.moveFile(fileMan.getSourceDir().getCurrentSrcDir()+separator+'package.mgx', directory+separator+"package.mgx")
                elif req["zipurl"]!="":
                    fileName = tools.generateSessionId()+".zip"
                    print("downloading ")
                    try:
                        netMan.downloadFile(req["zipurl"], fileName)
                        print("installing")
                        fileMan.unzip(fileName, directory)
                        #loader = ProgressLoader(total=100)
                        #loader.progress(100)
                        print("\n")
                        fileMan.delFile(fileName)
                        print(currentArg, " project created in the following directory :", directory)
                        packages["projects"]+=currentArg
                        packages["projects"]+=" "
                        with open(fileMan.getSourceDir().getCurrentSrcDir()+separator+'package.mgx', 'w') as outfile:
                            json.dump(packages, outfile)
                        fileMan.moveFile(fileMan.getSourceDir().getCurrentSrcDir()+separator+'package.mgx', directory+separator+"package.mgx")    

                    except Exception as e:
                        print("Something went wrong")
                    #print("this version is not yet compatible with the installation of this package try to upgrade mpm")
                else:
                    print("problem to download required packages")    

            else:
                print(currentArg, "not found in projects")
        else:
            print("problem to contact the database. Run mpm -u to solve the problem")    
        
    elif args.install:
        currentArg = args.install
        if db:
            db = json.loads(db)
            try:
                found = tools.in_json_array(currentArg, "name", db["modules"])
            except Exception as e:
                print("Something went wrong : problem to contact the database")
                exit()


            if(found[0]):
                req = db["modules"][found[1]]
                directory = currentArg if not args.d else args.d
                print("installing ", currentArg, " module")
                if req["git"]!="":
                    print("downloading and installing")
                    if netMan.gitClone(req["git"], directory):
                        print(res["process_completed"])
                        print("\n")
                        print("Module installed")
                        packages["modules"]+=currentArg
                        packages["modules"]+=" "
                        with open(fileMan.getSourceDir().getCurrentSrcDir()+separator+'package.mgx', 'w') as outfile:
                            json.dump(packages, outfile)

                        fileMan.moveFile(fileMan.getSourceDir().getCurrentSrcDir()+separator+'package.mgx', directory+separator+"package.mgx")
                elif req["zipurl"]!="":
                    fileName = tools.generateSessionId()+".zip"
                    print("downloading ")
                    try:
                        netMan.downloadFile(req["zipurl"], fileName)
                        print("installing")

                        fileMan.unzip(fileName, directory)
                        #loader = ProgressLoader(total=100)
                        #loader.progress(100)
                        print("\n")
                        fileMan.delFile(fileName)
                        print(args.install, " module installed")
                        packages["modules"]+=currentArg
                        packages["modules"]+=" "
                        with open(fileMan.getSourceDir().getCurrentSrcDir()+separator+'package.mgx', 'w') as outfile:
                            json.dump(packages, outfile)
                        fileMan.moveFile(fileMan.getSourceDir().getCurrentSrcDir()+separator+'package.mgx', directory+separator+"package.mgx")    

                    except Exception as e:
                        print("Something went wrong")
                    #print("this version is not yet compatible with the installation of this package try to upgrade mpm")
                else:
                    print("problem to download required packages")    

            else:
                print(currentArg, "not found in modules")
        else:
            print("problem to contact the database. Run mpm -update to solve the problem")        
    elif args.clone:
        currentArg = args.clone
        fileName = tools.generateSessionId()+".zip"
        directory = currentArg if not args.d else args.d
        print("cloning ", currentArg)
        try:
            netMan.downloadFile(req["zipurl"], fileName)
            print("installing")
            fileMan.unzip(fileName, directory)
            print("\n")
            fileMan.delFile(fileName)
            print(args.install, " cloned perfectly")
            packages["cloned"]+=currentArg
            packages["cloned"]+=" "
            with open(fileMan.getSourceDir().getCurrentSrcDir()+separator+'package.mgx', 'w') as outfile:
                json.dump(packages, outfile)
            fileMan.moveFile(fileMan.getSourceDir().getCurrentSrcDir()+separator+'package.mgx', directory+separator+"package.mgx")    

        except Exception as e:
            print("Something went wrong while cloning: the url miight be broken or your internet connection too slow")
    elif args.fileload:
        currentArg = args.fileload
        
        directory = currentArg if not args.d else args.d
        url = urlparse(currentArg)
        fileName = os.path.basename(url.path)
        print("cloning ", currentArg, "\n")

        
        try:
            netMan.downloadFile(currentArg, fileName)
            print("file saved with the following name", fileName)
        except Exception as e:
            print("Something went wrong while cloning")

    elif args.update:
        print("updating mpm this will uninstall the old version before installing the new")
        db = netMan.readFileFromUrl(gb.getFundInfos("url"))
        if not isinstance(db, bool):
            try:

                db = json.loads(bytearray(str(db),"utf-8"))
                if myOs == "windows":
                    print("download lastest mpm version by clicking on the following link", db[myOs])
                else:
                    url = db[myOs]
                    #os.system("mpm -uninstall")
                    os.system("cd /tmp && wget "+db[myOs]+" && unzip mpm.zip && cd mpm/ && ./install.sh && cd ../ && sudo rm mpm.zip && sudo rm -r mpm")                
                    
            except Exception as e:
                print("Something went wrong while updating")
                
        else:
            print("Something went wrong while updating")
            #print(e)
            exit()    
            

    elif args.bored:

        print("uninstalling mpm")

        if myOs == "windows":
            os.system("The uninstalling process is not still working on your mpm version. Go to the mpm installtion directory and run uninstall.exe file")
        else:
            os.system("sudo chmod +777 /usr/local/sbin/mpm_tools/uninstall.sh && cd /usr/local/sbin/mpm_tools && sudo ./uninstall.sh")
        


    else:
        print("command not found try mpm --help")        
        
    """
    elif args.update:
        print("updating mpm this will uninstall the old version before installing the new")
        db = netMan.readFileFromUrl(gb.getFundInfos("url"))
        if not isinstance(db, bool):
            try:

                db = json.loads(bytearray(str(db),"utf-8"))
                if myOs == "windows":
                    print("download last mpm version by clicking on the following link", db[myOs])
                else:
                    url = db[myOs]
                    #os.system("mpm -uninstall")
                    os.system("cd /tmp && wget "+db[myOs]+" && unzip mpm.zip && cd mpm && ./install.sh && cd ../ && sudo rm mpm.zip && sudo rm -r mpm")                
                    
            except Exception as e:
                print("Something went wrong while updating")
                
        else:
            print("Something went wrong while updating")
            #print(e)
            exit()       
             
    elif args.uninstall:

        print("uninstalling mpm")

        if myOs == "windows":
            os.system(fileMan.getSourceDir().getCurrentSrcDir()+"uninstall.exe")
        else:
            os.system("sudo chmod +777 /usr/local/sbin/mpm_tools/uninstall.sh && sudo ./usr/local/sbin/mpm_tools/uninstall.sh")
        
    
    elif args.version:
        print("the installed version of mpm is: ", gb.getFundInfos("version"))   
    """    
        
    
