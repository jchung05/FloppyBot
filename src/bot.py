import requests
import json

class FloppyBot(object):
    def __init__(self, url, role):
        self.__HOOK = url
        self.__ROLE_ID = role
        self.data = {
            "username" : "FloppyBot",
            "content" : None
        }

        # k,v => timestamp,{channel}
        self.__queue = dict()
        self.__garbage = set()

    # Sends message from queue and adds that item to garbage pile
    def sendMessage(self):
        for k,v in list(self.__queue.items()):
            # TODO: Add location and name later "@ {v.location} - {v.name}"
            self.data["content"] = '<@&{}> @ xx:{} ch{}'.format(self.__ROLE_ID,k,v["channel"])
            requests.post(self.__HOOK, data=json.dumps(self.data), headers={"Content-Type": "application/json"})

            self.__garbage.add(k)
            self.__queue.pop(k)

    # Does not take multiple users in one timestamp currently
    # If the timestamp already exists in queue or in the garbage, move on
    def enqueue(self, time:str, body:object):
        if 0 > int(time) or int(time) >= 60:
            return None
        if not self.__queue.get(time) and not time in self.__garbage:
            self.__queue[time] = body

    # 15 minute limit on garbage clean up
    def garbagePickup(self, time:int):
        for item in list(self.__garbage):
            _int = int(item)
            if time > _int and time - _int > 15:
                self.__garbage.remove(item)
            elif _int > time and 15 < time + 60 - _int < 45:
                self.__garbage.remove(item)

    @property
    def queue(self):
        return self.__queue

    @queue.setter
    def queue(self, value):
        self.__queue = value

    @property
    def garbage(self):
        return self.__garbage

    @garbage.setter
    def garbage(self, value):
        self.__garbage = value

    @property
    def hook(self):
        return self.__HOOK

    @hook.setter
    def hook(self, value):
        self.__HOOK = value

    @property
    def role(self):
        return self.__ROLE_ID

    @role.setter
    def role(self, value):
        self.__ROLE_ID = value