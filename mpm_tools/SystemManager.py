import os


class SystemManager:
    def getActualPath(self):
        return str(os.path.realpath(__file__).replace("/tools/SystemManager.py", ""))
