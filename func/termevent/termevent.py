from datetime import datetime
import json

class TermEvent:
    """
    member values:
        current_event:
            현재 이벤트에 대한 정보
        future_event:
            다음 이벤트에 대한 정보
    """
    __slots__ = ["current_event", "future_event"]

    def __init__(self):
        self.current_event = {}
        self.future_event = {}

    def _update_event(self, now: datetime, event_list: list) -> (dict, dict):
        result = ({}, {})

        for idx, _ in enumerate(event_list[:-1]):
            cure = event_list[idx]
            fute = event_list[idx+1]

            cure["to"] = datetime.strptime(cure["to"], "%Y-%m-%dT%H:%M:%S")
            cure["from"] = datetime.strptime(cure["from"], "%Y-%m-%dT%H:%M:%S")

            if(cure["from"] < now and now < cure["to"]):
                result = (cure, fute)
                if fute != {}:
                    fute["to"] = datetime.strptime(fute["to"], "%Y-%m-%dT%H:%M:%S")
                    fute["from"] = datetime.strptime(fute["from"], "%Y-%m-%dT%H:%M:%S")
                break
            
        return result