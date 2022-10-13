import json, requests, shutil

class UWCSEA():
    def __init__(self, name, username, password):
        self.query = name
        self.searched = False

        payload = f"Fingerprint=&ReturnUrl=&Username={username}&Password={password}"

        headers = {
            'authority': 'webapps.uwcsea.edu.sg',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': '',
            'origin': 'https://webapps.uwcsea.edu.sg',
            'referer': 'https://webapps.uwcsea.edu.sg/cims/Account/Login',
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }

        self.session = requests.session()
        self.session.post("https://webapps.uwcsea.edu.sg/cims/Account/Login", headers=headers, data=payload)

        with open("directory.json") as file:
            self.fileContent = json.load(file)
            
        self.searchByName()
    
    def searchByName(self):
        found = False
        for person in self.fileContent:
            if self.query.lower() in person["name"].lower():
                self.actualName = person["name"]
                self.searched = True
                self.file = person
                self.getUserID()
                return True

        if not found:
            return False

    def provideBasicInfo(self):
        if self.searched:
            self.getUserID()
            return [self.file["name"], self.file["email"], int(self.file["id"])]
        else:
            return False

    def getUserID(self):
        try:
            int(self.file["email"][self.file["email"].index("@gapps.uwcsea.edu.sg")-6])
            id = self.file["email"][self.file["email"].index("@gapps.uwcsea.edu.sg")-6: self.file["email"].index("@gapps.uwcsea.edu.sg")]
        except:
            id = self.file["email"][self.file["email"].index("@gapps.uwcsea.edu.sg")-5: self.file["email"].index("@gapps.uwcsea.edu.sg")]

        self.file["id"] = id

    def downloadStudentImage(self):
        imgresp = self.session.get("https://webapps.uwcsea.edu.sg/cims/Main/ViewPhoto?eid="+self.file["id"], stream=True)
        with open(str(self.file["id"])+".png", "wb") as out_file:
            shutil.copyfileobj(imgresp.raw, out_file)
