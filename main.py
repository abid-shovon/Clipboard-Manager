import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from pynput import keyboard

class ClipboardItem:
    def __init__(self, data_type, content):
        self.data_type = data_type  # 'text' or 'image'
        self.content = content

class ClipboardManager(QtWidgets.QWidget):
    MAX_HISTORY = 100

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clipboard Manager")
        self.setGeometry(100, 100, 500, 400)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Window)

        self.clipboard = QtWidgets.QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.on_clipboard_change)

        self.history = []
        self.list_widget = QtWidgets.QListWidget()

        # Set larger font
        font = QtGui.QFont()
        font.setPointSize(12)
        self.list_widget.setFont(font)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

        # Connect double click on list item to copy function
        self.list_widget.itemDoubleClicked.connect(self.copy_selected_item)

        # System tray setup
        self.tray_icon = QtWidgets.QSystemTrayIcon(QtGui.QIcon.fromTheme("edit-paste"), self)
        self.tray_icon.setToolTip("Clipboard Manager")
        tray_menu = QtWidgets.QMenu()
        restore_action = tray_menu.addAction("Show Clipboard Manager")
        quit_action = tray_menu.addAction("Quit")

        restore_action.triggered.connect(self.show_window)
        quit_action.triggered.connect(QtWidgets.QApplication.quit)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Global hotkey listener
        self.listener = keyboard.GlobalHotKeys({
            '<alt>+v': self.show_window
        })
        self.listener.start()

    def closeEvent(self, event):
        # minimize to tray instead of closing
        event.ignore()
        self.hide()

    def show_window(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def on_clipboard_change(self):
        mime = self.clipboard.mimeData(QtGui.QClipboard.Clipboard)
        self.handle_mime_data(mime)
        primary_mime = self.clipboard.mimeData(QtGui.QClipboard.Selection)
        self.handle_mime_data(primary_mime)

    def handle_mime_data(self, mime):
        if mime.hasImage():
            image = self.clipboard.image()
            if not image.isNull():
                self.add_to_history(ClipboardItem("image", image))
        elif mime.hasText():
            text = mime.text()
            if text.strip():
                self.add_to_history(ClipboardItem("text", text))

    def add_to_history(self, item):
        # avoid duplicates
        if item.data_type == "text" and any(i.data_type == "text" and i.content == item.content for i in self.history):
            return
        if item.data_type == "image" and any(i.data_type == "image" and i.content == item.content for i in self.history):
            return

        if len(self.history) >= self.MAX_HISTORY:
            self.history.pop()
            self.list_widget.takeItem(self.list_widget.count() - 1)

        self.history.insert(0, item)

        list_item = QtWidgets.QListWidgetItem()
        if item.data_type == "text":
            display_text = item.content if len(item.content) < 100 else item.content[:100] + "..."
            list_item.setText(display_text)
            list_item.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_FileIcon))
            list_item.setToolTip(item.content)  # Tooltip with full text
        elif item.data_type == "image":
            pixmap = QtGui.QPixmap.fromImage(item.content)
            pixmap = pixmap.scaled(64, 64, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            list_item.setIcon(QtGui.QIcon(pixmap))
            list_item.setText("[Image]")
            list_item.setToolTip("[Image data]")

        self.list_widget.insertItem(0, list_item)

    def copy_selected_item(self, item):
        if item.text() != "[Image]":
            # Copy full original text from history (not truncated display text)
            # Find corresponding ClipboardItem from self.history by matching display text start
            # Safer: match tooltip text instead
            for clip_item in self.history:
                if clip_item.data_type == "text":
                    tooltip_text = clip_item.content
                    # match tooltip of list item
                    if tooltip_text.startswith(item.text().rstrip("...")):
                        self.clipboard.setText(tooltip_text)
                        break

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    manager = ClipboardManager()
    manager.show()
    sys.exit(app.exec_())


