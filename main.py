import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from pynput.keyboard import GlobalHotKeys
import threading

class ClipboardItem:
    def __init__(self, data_type, content):
        self.data_type = data_type
        self.content = content

class ClipboardManager(QtWidgets.QWidget):
    MAX_HISTORY = 100

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clipboard History Manager")
        self.resize(600, 400)
        self.history = []

        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.setIconSize(QtCore.QSize(64, 64))
        self.list_widget.itemClicked.connect(self.paste_item)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

        self.clipboard = QtWidgets.QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.on_clipboard_change)

        self.last_clipboard_content = None

    def on_clipboard_change(self):
        mime = self.clipboard.mimeData()
        if mime.hasImage():
            image = self.clipboard.image()
            if not image.isNull():
                if self.last_clipboard_content != ("image", image):
                    self.add_to_history(ClipboardItem("image", image))
                    self.last_clipboard_content = ("image", image)
        elif mime.hasText():
            text = mime.text()
            if text.strip() and self.last_clipboard_content != ("text", text):
                self.add_to_history(ClipboardItem("text", text))
                self.last_clipboard_content = ("text", text)

    def add_to_history(self, item):
        if len(self.history) >= self.MAX_HISTORY:
            self.history.pop(0)
            self.list_widget.takeItem(0)

        self.history.append(item)

        list_item = QtWidgets.QListWidgetItem()
        if item.data_type == "text":
            display_text = item.content if len(item.content) < 100 else item.content[:100] + "..."
            list_item.setText(display_text)
            list_item.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_FileIcon))
        elif item.data_type == "image":
            pixmap = QtGui.QPixmap.fromImage(item.content)
            pixmap = pixmap.scaled(64, 64, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            list_item.setIcon(QtGui.QIcon(pixmap))
            list_item.setText("[Image]")
        self.list_widget.addItem(list_item)

    def paste_item(self, item):
        idx = self.list_widget.row(item)
        clipboard_item = self.history[idx]

        if clipboard_item.data_type == "text":
            self.clipboard.setText(clipboard_item.content)
        elif clipboard_item.data_type == "image":
            self.clipboard.setImage(clipboard_item.content)

        self.hide()

    def show_history(self):
        self.show()
        self.raise_()
        self.activateWindow()

def hotkey_thread(manager):
    def on_activate():
        QtCore.QMetaObject.invokeMethod(manager, "show_history", QtCore.Qt.QueuedConnection)

    from pynput.keyboard import GlobalHotKeys
    with GlobalHotKeys({
        '<alt>+v': on_activate
    }) as h:
        h.join()

def main():
    app = QtWidgets.QApplication(sys.argv)
    manager = ClipboardManager()

    t = threading.Thread(target=hotkey_thread, args=(manager,), daemon=True)
    t.start()

    sys.exit(app.exec_())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    window.show()
    sys.exit(app.exec_())

