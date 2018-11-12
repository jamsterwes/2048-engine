import eel


class Dashboard:
    def __init__(self, q, board_count=8):
        eel.init('web')

        # Add subclass's onload function
        @eel.expose
        def onload():
            eel.initBoards(board_count)
            self.onload(q)

    def run(self, q):
        eel.start('sboard.html', block=True)

    def update(self, data):
        eel.update(data[0], data[1], data[2])

    def onload(self, queue):
        while True:
            data = queue.get(timeout=None)
            self.update(data)
            eel.sleep(0.1)
