class Chapter:
    work = ""
    title = ""
    serial = 0
    content = ""

    def __init__(self, serial, title, content, work="UNTITLED"):
        self.content = content
        self.title = title
        self.work = work
        self.serial = serial

    def __repr__(self):
        return f"<Chapter {self.serial} [W: {self.work}] [T: {self.title}]>"
