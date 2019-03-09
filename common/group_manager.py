class Manager():
    def __init__(self, group):
        self.group = group

    def all_members(self):
        list = []
        for member in self.group.members:
            list.append({"id": member.puid, "name": member.name})
        return list
