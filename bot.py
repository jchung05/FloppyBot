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
    def enqueue(self, time:int, body:object):
        if not self.__queue.get(time) and not time in self.__garbage:
            self.__queue[time] = body

    # 15 minute limit on garbage clean up
    def garbagePickup(self, time:int):
        for item in list(self.__garbage):
            if time > item and time - item > 15:
                self.__garbage.remove(item)
            elif item > time and 15 < time + 60 - item < 45:
                self.__garbage.remove(item)