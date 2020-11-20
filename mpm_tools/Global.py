import os
class Global:
    def __init__(self):
        self.all = {
            "url": "https://arielassistance.com/mpm/database.json",
            "os": str(os.uname().sysname).lower(),
            "lang": "en",
            "version": "1.0",
            "responses": {
            "des": "test",
            "process_completed": "Completed  ████████████████████████████████ 100%"
            }
        }

    def getFundInfos(self, info):
        return self.all[info]
