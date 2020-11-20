import zipfile
import os
import tempfile
import shutil
from progress.bar import Bar


class FileManager:
    def __init__(self):
        self.sourceDir = ""

    def getSourceDir(self):
        self.sourceDir = os.getcwd()
        return self

    def setSrcDir(self, srcDir=""):

        self.sourceDir = os.path.dirname(os.path.realpath(__file__)) if srcDir=="" else srcDir
        
        return self


    def unzip(self, path_to_zip_file, directory_to_extract_to=""):
        """
        with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
            zip_ref.extractall(directory_to_extract_to)
        """
        zf = zipfile.ZipFile(path_to_zip_file)

        uncompress_size = sum((file.file_size for file in zf.infolist()))

        extracted_size = 0

        for file in zf.infolist():
            extracted_size += file.file_size
            inter = round(extracted_size * 100/uncompress_size)
            bar = Bar('Processing', max=100)
            for i in range(0, inter):
                bar.next()
            bar.finish()
            
            if directory_to_extract_to!="":
                zf.extract(file, directory_to_extract_to)
            else:
                zf.extract(file)

    def getFileContent(self, fileDir, root="___"):
        fileToRead = self.sourceDir+fileDir if root=="___" else root+fileDir

        print(fileToRead)
        if os.path.isfile(fileToRead):
            with open(fileToRead, "r") as file:
                state = file.read()
        else:
            state = False

        return state

    def writeFileContent(self, fileName, content, root="__"):
        fileToWrite = self.sourceDir+fileName if root=="___" else root+fileName
        #print(fileToRead)
        file = open(fileName, 'wb')
        file.write(bytearray(str(content), 'utf-8'))
        file.close()

    def createDir(self, dirName):
        if not os.path.exists(dirName):
            os.mkdir(dirName)

    def delDir(self, dirName):
        if os.path.isdir(dirName):
            shutil.rmtree(dirName)

    def createFile(self, fileName, content = ""):
        if not os.path.isfile(fileName):
            file = open(fileName, 'wb')
            if content!="":
                file.write(bytearray(str(content), 'utf-8'))
            file.close()
            
    def delFile(self, fileName):
        if os.path.isfile(fileName):
            os.remove(fileName)

    def createTmpDir(self):
        return tempfile.TemporaryDirectory()

    def createTmpFile(self):
        return tempfile.NamedTemporaryFile()


    def getCurrentSrcDir(self):
        return self.sourceDir

    def moveFile(self, path, newPath):
        shutil.move(path, newPath)
        return self