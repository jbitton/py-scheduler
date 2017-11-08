from collections import deque


class DES(object):
    def __init__(self):
        self.event_list = deque([])

    def put_event(self, new_event):
        if not self.event_list:
            self.event_list.appendleft(new_event)
            return

        for i, event in enumerate(self.event_list):
            if event.timestamp > new_event.timestamp:
                self.event_list.insert(i, new_event)
                return

        self.event_list.append(new_event)

    def get_event(self):
        if not self.event_list:
            return None
        return self.event_list.popleft()

    def get_next_event_time(self):
        if not self.event_list:
            return -1
        return self.event_list[0].timestamp
