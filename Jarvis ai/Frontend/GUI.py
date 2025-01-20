from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton ,QFrame , QLabel , QSizePolicy)

from PyQt5.QtGui import (
    QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap,
    QTextBlockFormat
)
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values
import sys
import os

# Load environment variables
env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")

# Define directory paths
current_dir = os.getcwd()
old_chat_message = "" 
TempDirPath = rf"{current_dir}\Frontend\Files"
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"

# Function to modify the answer by removing empty lines
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# Function to modify the query
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = [
        "how", "what", "who", "where", "when", "why", "which", "whose",
        "whom", "can you", "what's", "where's", "how's"
    ]

    if any(word in new_query for word in question_words):
        if query_words[-1][-1] not in ['.', '?', '!']:
            new_query += "?"
    else:
        if query_words[-1][-1] not in ['.', '?', '!']:
            new_query += '.'

    return new_query.capitalize()

def SetMicrophoneStatus(Command):
    with open(rf'{TempDirPath}\Mic.data', "w", encoding='utf-8') as file:
        file.write(Command)


def GetMicrophoneStatus():
    with open(rf'{TempDirPath}\Mic.data', "r", encoding='utf-8') as file:
        Status = file.read()
    return Status


def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}\Status.data', "w", encoding='utf-8') as file:
        file.write(Status)


def GetAssistantStatus():
    with open(rf'{TempDirPath}\Status.data', "r", encoding='utf-8') as file:
        Status = file.read()
    return Status


def MicButtonInitialed():
    SetMicrophoneStatus("False")


def MicButtonClosed():
    SetMicrophoneStatus("True")


def GraphicsDirectoryPath(Filename):
    Path = rf'{GraphicsDirPath}\{Filename}'
    return Path


def TempDirectoryPath(Filename):
    Path = rf'{TempDirPath}\{Filename}'
    return Path


def ShowTextToScreen(Text):
    with open(rf'{TempDirPath}\Responses.data', "w", encoding='utf-8') as file:
        file.write(Text)


class ChatSection(QWidget):
    def __init__(self):
        super(ChatSection, self).__init__()
        
        # Layout configuration
        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10, 40, 40, 100)
        layout.setSpacing(-10)

        # Chat text edit widget
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        
        # Set font for chat text edit
        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)

        # Set text color configuration
        text_color_format = QTextCharFormat()
        text_color_format.setForeground(QColor(Qt.blue))
        self.chat_text_edit.setCurrentCharFormat(text_color_format)

        layout.addWidget(self.chat_text_edit)

        # GIF label
        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border: none;")
        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
        movie.setScaledSize(QSize(480, 270))  # Set maximum GIF size
        self.gif_label.setMovie(movie)


        movie.start()
        layout.addWidget(self.gif_label)

        # Text label below the GIF
        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size: 16px; margin-right: 195px; border: none; margin-top: -30px;")
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)

        # Set background color
        self.setStyleSheet("background-color: black;")

        # Custom scrollbar styling
        self.chat_text_edit.setStyleSheet("""
        QScrollBar:vertical {
            border: none;
            background: black;
            width: 10px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background: white;
            min-height: 20px;
        }
        QScrollBar::add-line:vertical {
            background: black;
            height: 10px;
        }
        QScrollBar::sub-line:vertical {
            background: black;
            height: 10px;
        }
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        """)

def loadMessages(self):
    global old_chat_message
    try:
        with open(TempDirectoryPath('Responses.data'), "r", encoding='utf-8') as file:
            messages = file.read()

        if messages and str(old_chat_message) != str(messages):
            self.addMessage(message=messages, color='White')
            old_chat_message = messages
    except FileNotFoundError:
        print("Responses.data file not found.")
    except Exception as e:
        print(f"Error loading messages: {e}")

def SpeechRecogText(self):
    try:
        with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
            messages = file.read()
        self.label.setText(messages)
    except FileNotFoundError:
        print("Status.data file not found.")
    except Exception as e:
        print(f"Error reading speech recognition text: {e}")

def load_icon(self, path, width=60, height=60):
    pixmap = QPixmap(path)
    if not pixmap.isNull():
        new_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(new_pixmap)
    else:
        print(f"Error loading icon: {path}")

def toggle_icon(self):
    try:
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath('mic.png'), 60, 60)
            MicButtonClosed()
        else:
            self.load_icon(GraphicsDirectoryPath('voice.png'), 60, 60)
            MicButtonInitialed()
        self.toggled = not self.toggled
    except Exception as e:
        print(f"Error toggling icon: {e}")

def addMessage(self, message, color):
    try:
        cursor = self.chat_text_edit.textCursor()
        text_format = QTextCharFormat()
        block_format = QTextBlockFormat()

        # Configure margins for the message
        block_format.setTopMargin(10)
        block_format.setLeftMargin(10)

        # Set the text color
        text_format.setForeground(QColor(color))

        # Apply formatting
        cursor.setCharFormat(text_format)
        cursor.setBlockFormat(block_format)

        # Insert the message with a newline
        cursor.insertText(message + "\n")

        # Ensure the cursor stays at the latest position
        self.chat_text_edit.setTextCursor(cursor)
    except Exception as e:
        print(f"Error adding message: {e}")
class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Get screen dimensions
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()

        # Set up the content layout
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Create a QLabel for the GIF
        gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
        gif_label.setMovie(movie)

        # Calculate maximum GIF size based on screen width and aspect ratio (16:9)
        max_gif_size_H = int(screen_width / 16 * 9)
        movie.setScaledSize(QSize(screen_width, max_gif_size_H))

        # Align the GIF to the center
        gif_label.setAlignment(Qt.AlignCenter)

        # Start the GIF animation
        movie.start()

        # Set size policy for the GIF label
        gif_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Set up the icon label
        self.icon_label = QLabel()
        pixmap = QPixmap(GraphicsDirectoryPath('Mic_on.png'))
        new_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(new_pixmap)
        self.icon_label.setFixedSize(150, 150)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.toggled = True
        self.toggle_icon()
        self.icon_label.mousePressEvent = self.toggle_icon

        # Set up the status label
        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px; margin-bottom:0;")

        # Add widgets to the layout
        content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        content_layout.setContentsMargins(0, 0, 0, 150)

        self.setLayout(content_layout)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        self.setStyleSheet("background-color: black;")

        # Timer setup
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)

    def SpeechRecogText(self):
        try:
            # Read status and update label text only if the file content changes
            with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
                messages = file.read()
                if messages != self.label.text():  # Update only if different
                    self.label.setText(messages)
        except FileNotFoundError:
            self.label.setText("Status file not found.")
        except Exception as e:
            self.label.setText(f"Error: {e}")

    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            new_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.icon_label.setPixmap(new_pixmap)
        else:
            print(f"Error loading icon: {path}")

    def toggle_icon(self, event=None):
        try:
            if self.toggled:
                self.load_icon(GraphicsDirectoryPath('Mic_off.png'), 60, 60)
                MicButtonClosed()
            else:
                self.load_icon(GraphicsDirectoryPath('Mic_on.png'), 60, 60)
                MicButtonInitialed()
            self.toggled = not self.toggled
        except Exception as e:
            print(f"Error toggling icon: {e}")

class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Get screen dimensions
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()

        # Set up the content layout
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Create a QLabel for the GIF
        gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
        gif_label.setMovie(movie)

        # Calculate maximum GIF size based on screen width and aspect ratio (16:9)
        max_gif_size_H = int(screen_width / 16 * 9)
        movie.setScaledSize(QSize(screen_width, max_gif_size_H))

        # Align the GIF to the center
        gif_label.setAlignment(Qt.AlignCenter)

        # Start the GIF animation
        movie.start()

        # Set size policy for the GIF label
        gif_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Set up the icon label
        self.icon_label = QLabel()
        pixmap = QPixmap(GraphicsDirectoryPath('Mic_on.png'))
        new_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(new_pixmap)
        self.icon_label.setFixedSize(150, 150)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.toggled = True
        self.toggle_icon()
        self.icon_label.mousePressEvent = self.toggle_icon

        # Set up the status label
        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size:16px; margin-bottom:0;")

        # Add widgets to the layout
        content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        content_layout.setContentsMargins(0, 0, 0, 150)

        self.setLayout(content_layout)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        self.setStyleSheet("background-color: black;")

        # Timer setup
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)

    def SpeechRecogText(self):
        try:
            # Read status and update label text only if the file content changes
            with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
                messages = file.read()
                if messages != self.label.text():  # Update only if different
                    self.label.setText(messages)
        except FileNotFoundError:
            self.label.setText("Status file not found.")
        except Exception as e:
            self.label.setText(f"Error: {e}")

    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            new_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.icon_label.setPixmap(new_pixmap)
        else:
            print(f"Error loading icon: {path}")

    def toggle_icon(self, event=None):
        try:
            if self.toggled:
                self.load_icon(GraphicsDirectoryPath('Mic_off.png'), 60, 60)
                MicButtonClosed()
            else:
                self.load_icon(GraphicsDirectoryPath('Mic_on.png'), 60, 60)
                MicButtonInitialed()
            self.toggled = not self.toggled
        except Exception as e:
            print(f"Error toggling icon: {e}")

class MessageScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Get screen dimensions
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()

        # Set up the main layout
        layout = QVBoxLayout()

        # Create a label widget
        label = QLabel("")

        # Add the label to the layout
        layout.addWidget(label)

        # Create a ChatSection instance
        chat_section = ChatSection()

        # Add the ChatSection to the layout
        layout.addWidget(chat_section)

        # Apply the layout to the widget
        self.setLayout(layout)

        # Set the background color
        self.setStyleSheet("background-color: black;")

        # Set the fixed dimensions of the screen
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)

        # Set up a timer
        self.timer = QTimer(self)

class CustomTopBar(QWidget):
    def __init__(self, parent=None, stacked_widget=None):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.setFixedHeight(50)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignRight)

        # Home button
        home_button = QPushButton()
        home_icon = QIcon(GraphicsDirectoryPath("Home.png"))
        home_button.setIcon(home_icon)
        home_button.setText("Home")
        layout.addStretch(1)  # Add stretchable space before the home button
        home_button.setStyleSheet("height:40px; line-height:40px; background-color: transparent; border: none;")
        layout.addWidget(home_button, alignment=Qt.AlignCenter)  # Center the home button
        layout.addStretch(1)  # Add stretchable space after the home button
        home_button.clicked.connect(self.showInitialScreen)
        layout.addWidget(home_button)

        # Message button (Chat)
        message_button = QPushButton()
        message_icon = QIcon(GraphicsDirectoryPath("Chats.png"))
        message_button.setIcon(message_icon)
        message_button.setText("Chat")
        message_button.setStyleSheet("height:40px; line-height:40px; background-color: white; color: black")
        message_button.clicked.connect(self.showMessageScreen)
        layout.addWidget(message_button)

        # Minimize button
        minimize_button = QPushButton()
        minimize_icon = QIcon(GraphicsDirectoryPath('Minimize2.png'))
        minimize_button.setIcon(minimize_icon)
        minimize_button.setStyleSheet("background-color:white")
        minimize_button.clicked.connect(self.minimizeWindow)
        layout.addWidget(minimize_button)

        # Maximize/Restore button
        self.maximize_button = QPushButton()
        self.maximize_icon = QIcon(GraphicsDirectoryPath('Maximize.png'))
        self.restore_icon = QIcon(GraphicsDirectoryPath('Minimize.png'))
        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.setFlat(True)
        self.maximize_button.setStyleSheet("background-color:white")
        self.maximize_button.clicked.connect(self.maximizeWindow)
        layout.addWidget(self.maximize_button)

        # Close button
        close_button = QPushButton()
        close_icon = QIcon(GraphicsDirectoryPath('Close.png'))
        close_button.setIcon(close_icon)
        close_button.setStyleSheet("background-color:white")
        close_button.clicked.connect(self.closeWindow)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)
        super().paintEvent(event)

    def minimizeWindow(self):
        self.parent().showMinimized()

    def maximizeWindow(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(self.maximize_icon)
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(self.restore_icon)

    def closeWindow(self):
        self.parent().close()

    def showInitialScreen(self):
        self.stacked_widget.setCurrentIndex(0)

    def showMessageScreen(self):
        self.stacked_widget.setCurrentIndex(1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()
        self.setWindowTitle("Main Window")

    def initUI(self):
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()

        stacked_widget = QStackedWidget(self)
        initial_screen = InitialScreen()
        message_screen = MessageScreen()

        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen)

        self.setGeometry(0, 0, screen_width, screen_height)
        self.setStyleSheet("background-color: black;")

        top_bar = CustomTopBar(self, stacked_widget)
        self.setMenuWidget(top_bar)

        self.setCentralWidget(stacked_widget)

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()  # Create the main window
    window.show()  # Show the window
    sys.exit(app.exec_())  # Run the application event loop

if __name__ == "__main__":
    GraphicalUserInterface()  # Run the GUI