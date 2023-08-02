from datetime import datetime
import json

class GDFConfiguration():
    def __init__(self, settings_json):
        self.settings_json = settings_json
        self.reload()

    def reload(self):
        f = open(self.settings_json)
        self.settings = json.load(f)
        self.current = self.getScene(self.getSelected())


    def getSelected(self):
        program = self.get("program")
        now = datetime.now()
        hour = now.strftime("%H")
        min = now.strftime("%M")
        for scene in program:
            start = scene['from'].split(':')
            start = datetime(1980, 2, 17, int(start[0]), int(start[1]), 0)
            end = scene['to'].split(':')
            end = datetime(1980, 2, 17, int(end[0]), int(end[1]), 0)
            if (now.time() >= start.time() and now.time() < end.time()):
                return scene['scene']
        scenes = self.get("scenes")
        return scenes[0]['name']

    def setCurrent(self,name):
        self.current = self.getScene(name)


    def appendScene(self,name):
        new_scene = {}
        new_scene["name"] = name
        new_scene["type"] = self.current["type"]
        self.settings["scenes"].append(new_scene)
        self.save()

    def save(self):
        with open(self.settings_json, 'w') as f:
            json.dump(self.settings, f, indent = 4)


    def get(self,path):
        keys = path.split('.')
        val = self.settings
        for key in keys:
            if key in val:
                val = val[key]
            else: return None
        return val
    
    def getScene(self,name):
        scenes = self.get("scenes")
        for scene in scenes:
            if (scene["name"] == name):
                return scene
        return None

    def update(self, path, value):
        keys = path.split('.')
        current_dict = self.settings
        for key in keys[:-1]:
            current_dict = current_dict[key]
        current_dict[keys[-1]] = value
