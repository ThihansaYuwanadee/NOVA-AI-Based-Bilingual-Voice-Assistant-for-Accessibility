import sys
import os

# --- FIX 1: Set this before importing PyQt5 to prevent COM conflict ---
os.environ["QT_IM_MODULE"] = "simple"
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox"
os.environ["QT_DISABLE_NATIVE_WINDOWS"] = "1"

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt, QPoint, pyqtSlot, QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWebChannel import QWebChannel
main_module_loaded = False
main = None



# This class acts as a bridge for JavaScript to call Python functions
class BackendBridge(QObject):
    themeChanged = pyqtSignal(str)
    micStatusChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(str)
    def setTheme(self, theme_name):
        print(f"Python backend received theme change: {theme_name}")
        self.themeChanged.emit(theme_name)

    @pyqtSlot(str)
    def micMode(self, micMode):
        print(f"Python backend received mic mode: {micMode}")


        global main, main_module_loaded
        if not main_module_loaded:
            import main  # Lazy import fixes COM race condition
            main_module_loaded = True

        main.start(micMode)
       


class HTMLApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NOVA AI")
        self.setGeometry(200, 100, 900, 600) # Reduced size

        # Remove native OS window frame
        self.setWindowFlags(Qt.FramelessWindowHint)
        # VERY IMPORTANT: Enable translucent background for the window itself
        # This allows the border-radius on child widgets to be visible
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.old_pos = None # For dragging the window

        # === Custom Title Bar ===
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(40)
        self.title_bar.setContentsMargins(0, 0, 0, 0)
        self.title_bar.setObjectName("titleBar") # Set object name for styling

         # as this Python script, or provide the full path to the image file.
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        
        # We use QIcon to load the image file
        app_icon = QIcon(icon_path) 
        
        # 2. Apply the Icon to the Window
        self.setWindowIcon(app_icon)

        # Title Label
        self.title_label = QLabel("NOVA AI")
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter) # Align left and vertically center
        self.title_label.setObjectName("titleLabel") # Object name for specific styling

        # Window control buttons - store references for dynamic styling
        self.btn_min = QPushButton("_")
        self.btn_max = QPushButton("⬜")
        self.btn_close = QPushButton("✕")

        for btn in (self.btn_min, self.btn_max, self.btn_close):
            btn.setFixedSize(40, 30)
            # Connect the buttons to their respective slots
        self.btn_min.clicked.connect(self.showMinimized)
        self.btn_max.clicked.connect(self.toggle_maximize_restore)
        self.btn_close.clicked.connect(self.close)

        title_layout = QHBoxLayout()
        title_layout.addWidget(self.title_label)
        title_layout.addStretch() # Pushes buttons to the right
        title_layout.addWidget(self.btn_min)
        title_layout.addWidget(self.btn_max)
        title_layout.addWidget(self.btn_close)
        title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_bar.setLayout(title_layout)

        # Make title bar draggable
        self.title_bar.mousePressEvent = self._title_bar_mousePressEvent
        self.title_bar.mouseMoveEvent = self._title_bar_mouseMoveEvent
        self.title_bar.mouseReleaseEvent = self._title_bar_mouseReleaseEvent


        # === Web View (HTML/CSS UI) ===
        self.browser = QWebEngineView()
        # Ensure the web folder is correctly referenced relative to this script
        html_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"web", "index.html"))
        self.browser.load(QUrl.fromLocalFile(html_path))

        # WebChannel to talk from JS to Python
        self.channel = QWebChannel()
        self.bridge = BackendBridge()
        self.channel.registerObject("backend", self.bridge)
        self.browser.page().setWebChannel(self.channel)
        # Connect the theme change signal from the bridge to our update method
        self.bridge.themeChanged.connect(self.update_widget_theme)

        # === Custom Lower Bar ===
        self.lower_bar = QWidget()
        self.lower_bar.setFixedHeight(30) # Fixed height for the lower bar
        self.lower_bar.setContentsMargins(0, 0, 0, 0)
        self.lower_bar.setObjectName("lowerBar") # Set object name for styling

        self.lower_bar_label = QLabel("")
        self.lower_bar_label.setAlignment(Qt.AlignCenter)
        
        lower_layout = QHBoxLayout()
        lower_layout.addStretch()
        lower_layout.addWidget(self.lower_bar_label)
        lower_layout.addStretch()
        lower_layout.setContentsMargins(10, 0, 10, 0)
        self.lower_bar.setLayout(lower_layout)

        # === Layout ===
        # Create a central container widget for the entire content (title bar + browser + lower bar)
        self.container = QWidget()
        self.container.setObjectName("centralContainer") # Set object name for styling
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.title_bar)
        layout.addWidget(self.browser)
        layout.addWidget(self.lower_bar) # Add the new lower bar here
        self.container.setLayout(layout)
        self.setCentralWidget(self.container) # Set this container as the central widget
        
        # Apply initial theme (default to dark, but HTML will inform us on load)
        self.update_widget_theme('dark-theme')

    def update_widget_theme(self, theme_name):
        """
        Applies appropriate QSS styles to the window frame, title bar, lower bar, and its buttons
        based on the provided theme_name, ensuring correct corner curls, gradients, and button colors.
        """
        # --- Theme-specific colors and gradients ---
        if theme_name == "dark-theme":
            container_bg_color = "rgba(10, 31, 58, 0.9);"
            title_label_text_color = "white;"
            lower_bar_text_color = "rgba(255, 255, 255, 0.7);"
            title_bar_gradient = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(15, 15, 15, 0.4), stop:1 rgba(35, 35, 35, 0.4));"
            lower_bar_gradient = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(10, 10, 10, 0.3), stop:1 rgba(30, 30, 30, 0.3));"
            
            # Button styles for dark theme
            min_max_button_qss = """
                QPushButton {
                    border: none;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 5px;
                    color: white;
                    background-color: rgba(52, 73, 94, 0.6);
                }
                QPushButton:hover {
                    background-color: rgba(85, 107, 130, 0.75);
                }
                QPushButton:pressed {
                    background-color: rgba(26, 42, 58, 0.85);
                }
            """
            close_button_qss = """
                QPushButton {
                    border: none;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 5px;
                    color: white;
                    background-color: rgba(231, 76, 60, 0.6);
                }
                QPushButton:hover {
                    background-color: rgba(192, 57, 43, 0.75);
                }
                QPushButton:pressed {
                    background-color: rgba(165, 42, 42, 0.85);
                }
            """

        elif theme_name == "light-theme":
            container_bg_color = "rgba(200, 230, 255, 0.9);"
            title_label_text_color = "#333;"
            lower_bar_text_color = "rgba(51, 51, 51, 0.7);"
            title_bar_gradient = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 192, 203, 0.2), stop:0.5 rgba(173, 216, 230, 0.2), stop:1 rgba(144, 238, 144, 0.2));"
            lower_bar_gradient = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 192, 203, 0.1), stop:0.5 rgba(173, 216, 230, 0.1), stop:1 rgba(144, 238, 144, 0.1));" 
            
            # Button styles for light theme
            min_max_button_qss = """
                QPushButton {
                    border: none;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 5px;
                    color: #333; /* Dark text for light mode buttons */
                    background-color: rgba(200, 210, 220, 0.2);
                }
                QPushButton:hover {
                    background-color: rgba(170, 180, 190, 0.35);
                }
                QPushButton:pressed {
                    background-color: rgba(140, 150, 160, 0.45);
                }
            """
            close_button_qss = """
                QPushButton {
                    border: none;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 5px;
                    color: white; /* Keep white for contrast on red background */
                    background-color: rgba(240, 100, 90, 0.2);
                }
                QPushButton:hover {
                    background-color: rgba(210, 70, 60, 0.35);
                }
                QPushButton:pressed {
                    background-color: rgba(180, 40, 30, 0.45);
                }
            """

        # --- Main Container Styling (includes title bar, browser, lower bar and labels) ---
        self.container.setStyleSheet(f"""
            #centralContainer {{ /* Target the main container widget */
                background-color: {container_bg_color};
                border-radius: 20px; /* Applies 20px radius to all four corners */
            }}
            #centralContainer QWidget#titleBar {{ /* Target the title bar within the container */
                border-top-left-radius: 20px;
                border-top-right-radius: 20px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
                background: {title_bar_gradient}; /* Apply gradient background */
            }}
            #centralContainer QWebEngineView {{
                border-radius: 0px; /* No rounded corners, as it's in the middle */
                background-color: transparent; /* Allows parent background to show through if needed */
            }}
            #centralContainer QWidget#lowerBar {{ /* Target the new lower bar within the container */
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
                border-bottom-left-radius: 20px;
                border-bottom-right-radius: 20px;
                background: {lower_bar_gradient}; /* Apply gradient background */
            }}
            #centralContainer QLabel {{ /* General QLabel styling for main container */
                color: {title_label_text_color}; 
            }}
            #centralContainer QLabel#titleLabel {{ /* Specific styling for the title label */
                font-weight: bold;
                font-size: 14px; /* Reduced font size to 14px */
                margin-left: 10px; /* Maintain left margin */
                color: {title_label_text_color}; /* Ensure text color matches theme */
            }}
            #centralContainer QWidget#lowerBar QLabel {{ /* Specific styling for lower bar label */
                color: {lower_bar_text_color};
                font-size: 11px; /* Smaller font for copyright notice */
                padding-right: 10px; 
                padding-left: 10px; 
            }}
        """)
        
        # --- Apply Control Button Styling ---
        self.btn_min.setStyleSheet(min_max_button_qss)
        self.btn_max.setStyleSheet(min_max_button_qss)
        self.btn_close.setStyleSheet(close_button_qss)


    def toggle_maximize_restore(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # === Dragging the window ===
    def _title_bar_mousePressEvent(self, event):
        # Check if the click is on any of the control buttons.
        # If it is, we let the button handle the event.
        if event.button() == Qt.LeftButton:
            # Convert event position to global coordinates and then to the button's local coordinates
            # to check if click is within button bounds.
            global_pos = self.title_bar.mapToGlobal(event.pos())

            if self.btn_min.geometry().contains(self.btn_min.mapFromGlobal(global_pos)) or \
               self.btn_max.geometry().contains(self.btn_max.mapFromGlobal(global_pos)) or \
               self.btn_close.geometry().contains(self.btn_close.mapFromGlobal(global_pos)):
                # If a button was clicked, don't start dragging.
                # Propagate the event so the button's click handler is called.
                return QWidget.mousePressEvent(self.title_bar, event)
            else:
                # If not on a button, start dragging.
                self.old_pos = event.globalPos()

    def _title_bar_mouseMoveEvent(self, event):
        if self.old_pos and not self.isMaximized():
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def _title_bar_mouseReleaseEvent(self, event):
        self.old_pos = None

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HTMLApp()
    window.show()
    sys.exit(app.exec_())