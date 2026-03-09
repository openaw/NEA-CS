import sys, os, json, hashlib
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QFrame, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QGridLayout, QListWidget, QListWidgetItem,
    QStackedWidget, QTableWidget, QTableWidgetItem, QDialog, QMessageBox, 
    QRadioButton, QScrollArea, QSizePolicy, QComboBox, QFormLayout, QSpinBox, QDoubleSpinBox
)

QSS = """
/* overall general theme. QSS will be ported via file later when accessibility settings implemented*/

/*##########Global##########*/
QWidget {
    background: #0f141b;
    color: #d7dde8;
    font-family: Inter, Segoe UI, Arial;
    font-size: 17px;
}

QLabel {
    background: transparent;
}

QMainWindow {
    background: #0f141b;
}

/* CSS styles for specifically targeted widgets */
/* # to identify for unique elements and . to identify styling over multiple widgets */

/*##########Sidebar##########*/
#Sidebar {
    background: #0b1016;
    border-right: 1px solid rgba(255,255,255,0.06);
}

#Brand {
    font-size: 28px;
    font-weight: 700;
    padding: 14px 14px;
    color: #eef3ff;
}

QListWidget#NavList {
    background: transparent;
    border: none;
    padding: 6px;
    outline: none;
}

QPushButton#ProfileFooter {
    text-align: left;
    background: #121a24;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
}

QListWidget#NavList::item {
    padding: 10px 12px;
    margin: 4px 6px;
    border-radius: 10px;
    color: rgba(215,221,232,0.90);
}

QListWidget#NavList::item:hover {
    background: rgba(255,255,255,0.05);
}

QListWidget#NavList::item:selected {
    background: rgba(118, 142, 255, 0.18);
    border: 1px solid rgba(118, 142, 255, 0.28);
    color: #f1f5ff;
}

QPushButton#ProfileFooter:hover {
    background: rgba(255,255,255,0.05);
}

QPushButton#ProfileFooter:pressed {
    background: rgba(255,255,255,0.03);
}

/*##########Content##########*/
#PageTitle {
    font-size: 35px;
    font-weight: 700;
    color: #eef3ff;
}

#Subtle {
    color: rgba(215,221,232,0.72);
}

/*##########Cards##########*/
.Card {
    background: #121a24;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
}

.CardTitle {
    font-size: 15px;
    font-weight: 700;
    color: rgba(238,243,255,0.95);
}

.CardKPI {
    font-size: 26px;
    font-weight: 800;
    color: #eef3ff;
}

.CardCaption {
    color: rgba(215,221,232,0.65);
}

/*##########Charts##########*/
.ChartBox {
    background: rgba(11,16,22,0.65);
    border: 1px dashed rgba(255,255,255,0.10);
    border-radius: 12px;
}

/*##########List##########*/
QTableWidget {
    background: transparent;
    border: none;
}

QHeaderView::section {
    background: rgba(11,16,22,0.65);
    border: none;
    padding: 8px 10px;
    font-weight: 700;
    color: rgba(238,243,255,0.95);
}

QTableWidget::item {
    padding: 8px 10px;
}

QTableWidget::item:selected {
    background: rgba(118, 142, 255, 0.18);
}

/*##########Item Cards########## */
.ItemCard {
    background: #121a24;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
}

.ItemCard:hover {
    background: rgba(118, 142, 255, 0.25);
    border: 1px solid rgba(118, 142, 255, 0.40);
}

.ItemCard:pressed {
    background: rgba(118, 142, 255, 0.14);
}

.ItemName {
    font-size: 16px;
    font-weight: 800;
    color: rgba(238,243,255,0.95);
}

.ItemQtyPrice {
    font-size: 13px;
    font-weight: 700;
    color: rgba(215,221,232,0.75);
}

.ItemImageFrame {
    background: rgba(11,16,22,0.6);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
}

/*##########Inputs / Buttons on pages##########*/
QLineEdit {
    background: #0b1016;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 9px 12px;
}

QPushButton {
    background: rgba(118, 142, 255, 0.18);
    border: 1px solid rgba(118, 142, 255, 0.28);
    border-radius: 10px;
    padding: 9px 12px;
    font-weight: 700;
}

QPushButton:hover {
    background: rgba(118, 142, 255, 0.25);
    border: 1px solid rgba(118, 142, 255, 0.40);
}

QPushButton:pressed {
    background: rgba(118, 142, 255, 0.14);
}

QComboBox, QSpinBox, QDoubleSpinBox {
    background: #0b1016;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 6px 10px;
}

QComboBox::drop-down {
    border: none;
}
"""


#Variables and functions concerning directories & linking files
ACCOUNTS_PATH = "accounts.json"

def app_dir():
    return os.path.dirname(os.path.realpath(__file__))

def images_dir():
    return os.path.join(app_dir(), "Images")

def load_accounts(path = ACCOUNTS_PATH):
    #return dict of accounts, false if file missing
    if not os.path.exists(path):
        return {}
    else:
        with open(path, "r") as file:
            data = json.load(file)
        return data


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class InitialAccountCreation(QDialog):
    def __init__(self, accounts_path = ACCOUNTS_PATH):
        super().__init__()
        self.accounts_path = accounts_path
        self.created_username = None

        self.setWindowTitle("Initial Account Creation - TrackStock")
        self.setModal(True)
        self.resize(520, 360)

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        title = QLabel("Create your admin account")
        title.setObjectName("PageTitle")

        hint = QLabel("No accounts found on this device. Create one to continue.")
        hint.setObjectName("Subtle")
        hint.setWordWrap(True)

        root.addWidget(title)
        root.addWidget(hint)

        card = QFrame()
        card.setProperty("class", "Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(10)

        form = QGridLayout()
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(10)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username (min 3 chars)")

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("Password (min 6 chars)")

        self.confirm = QLineEdit()
        self.confirm.setEchoMode(QLineEdit.Password)
        self.confirm.setPlaceholderText("Confirm password")

        form.addWidget(QLabel("Username"), 0, 0)
        form.addWidget(self.username, 0, 1)
        form.addWidget(QLabel("Password"), 1, 0)
        form.addWidget(self.password, 1, 1)
        form.addWidget(QLabel("Confirm"), 2, 0)
        form.addWidget(self.confirm, 2, 1)

        card_layout.addLayout(form)

        btn_row = QHBoxLayout()
        btn_row.addStretch(1)

        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(self.reject)

        create_btn = QPushButton("Create account")
        create_btn.clicked.connect(self.create_account)

        btn_row.addWidget(exit_btn)
        btn_row.addWidget(create_btn)

        card_layout.addLayout(btn_row)
        root.addWidget(card)

    def create_account(self):
        u = self.username.text().strip()
        p = self.password.text()
        c = self.confirm.text()

        if len(u) < 3:
            QMessageBox.warning(self, "Invalid username", "Username must be at least 3 characters.")
            return
        if len(p) < 6:
            QMessageBox.warning(self, "Weak password", "Password must be at least 6 characters.")
            return
        if p != c:
            QMessageBox.warning(self, "Mismatch", "Passwords do not match.")
            return

        accounts = load_accounts(self.accounts_path)
        accounts[u] = {"password_hash": hash_password(p),
                       "user_level": "Super Admin"}
        with open(self.accounts_path, "w") as f:
            json.dump(accounts, f, indent=2)

        self.created_username = u
        self.accept()

class SignIn(QDialog):
    def __init__(self, accounts_path = ACCOUNTS_PATH):
        super().__init__()
        self.accounts_path = accounts_path
        self.signed_in_username = None

        self.setWindowTitle("Sign In - TrackStock")
        self.setModal(True)
        self.resize(520, 320)

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        title = QLabel("Sign in")
        title.setObjectName("PageTitle")

        hint = QLabel("Enter your username and password to continue.")
        hint.setObjectName("Subtle")
        hint.setWordWrap(True)

        root.addWidget(title)
        root.addWidget(hint)

        card = QFrame()
        card.setProperty("class", "Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(10)

        form = QGridLayout()
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(10)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("Password")

        form.addWidget(QLabel("Username"), 0, 0)
        form.addWidget(self.username, 0, 1)
        form.addWidget(QLabel("Password"), 1, 0)
        form.addWidget(self.password, 1, 1)

        card_layout.addLayout(form)

        btn_row = QHBoxLayout()
        btn_row.addStretch(1)

        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(self.reject)

        sign_in_btn = QPushButton("Sign in")
        sign_in_btn.clicked.connect(self.sign_in)

        btn_row.addWidget(exit_btn)
        btn_row.addWidget(sign_in_btn)

        card_layout.addLayout(btn_row)
        root.addWidget(card)

    def sign_in(self):
        u = self.username.text().strip()
        p = self.password.text()

        accounts = load_accounts(self.accounts_path)
        if u not in accounts:
            QMessageBox.warning(self, "Sign in failed", "Unknown username.")
            return

        expected = accounts[u].get("password_hash")
        if hash_password(p) != expected:
            QMessageBox.warning(self, "Sign in failed", "Incorrect password.")
            return

        self.signed_in_username = u
        self.signed_in_userlevel = accounts[u].get("user_level")
        self.accept()

class CreateAccount(QDialog):
    def __init__(self, accounts_path=ACCOUNTS_PATH):
        super().__init__()
        self.accounts_path = accounts_path

        self.setWindowTitle("Create Account - TrackStock")
        self.setModal(True)
        self.resize(520, 420)

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        title = QLabel("Create an account")
        title.setObjectName("PageTitle")

        hint = QLabel("Create an Admin or Standard account.")
        hint.setObjectName("Subtle")
        hint.setWordWrap(True)

        root.addWidget(title)
        root.addWidget(hint)

        card = QFrame()
        card.setProperty("class", "Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(10)

        form = QGridLayout()
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(10)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username (min 3 chars)")

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("Password (min 6 chars)")

        self.confirm = QLineEdit()
        self.confirm.setEchoMode(QLineEdit.Password)
        self.confirm.setPlaceholderText("Confirm password")

        form.addWidget(QLabel("Username"), 0, 0)
        form.addWidget(self.username, 0, 1)
        form.addWidget(QLabel("Password"), 1, 0)
        form.addWidget(self.password, 1, 1)
        form.addWidget(QLabel("Confirm"), 2, 0)
        form.addWidget(self.confirm, 2, 1)

        card_layout.addLayout(form)

        #role radio buttons (rb)
        role_row = QHBoxLayout()
        role_row.setSpacing(12)

        role_label = QLabel("Account type")
        self.rb_admin = QRadioButton("Admin")
        self.rb_standard = QRadioButton("Standard")
        self.rb_standard.setChecked(True)

        role_row.addWidget(role_label)
        role_row.addStretch(1)
        role_row.addWidget(self.rb_admin)
        role_row.addWidget(self.rb_standard)

        card_layout.addLayout(role_row)

        btn_row = QHBoxLayout()
        btn_row.addStretch(1)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)

        create_btn = QPushButton("Create account")
        create_btn.clicked.connect(self.create_account)

        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(create_btn)

        card_layout.addLayout(btn_row)
        root.addWidget(card)

    def create_account(self):
        u = self.username.text().strip()
        p = self.password.text()
        c = self.confirm.text()

        if len(u) < 3:
            QMessageBox.warning(self, "Invalid username", "Username must be at least 3 characters.")
            return
        if len(p) < 6:
            QMessageBox.warning(self, "Weak password", "Password must be at least 6 characters.")
            return
        if p != c:
            QMessageBox.warning(self, "Mismatch", "Passwords do not match.")
            return

        accounts = load_accounts(self.accounts_path)
        if u in accounts:
            QMessageBox.warning(self, "Username exists", "That username already exists.")
            return
        
        if self.rb_admin.isChecked():
            user_level = "Admin"
        else:
            user_level = "Standard"

        accounts[u] = {
            "password_hash": hash_password(p),
            "user_level": user_level
        }
        with open(self.accounts_path, "w") as f:
            json.dump(accounts, f, indent=2)
        self.accept()

class Settings(QDialog):
    def __init__(self, current_user_level, accounts_path=ACCOUNTS_PATH):
        super().__init__()
        self.current_user_level = current_user_level
        self.accounts_path = accounts_path

        self.setWindowTitle("Settings")
        self.setModal(True)
        self.resize(420, 260)

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(12)

        title = QLabel("Settings")
        title.setObjectName("PageTitle")
        root.addWidget(title)

        hint = QLabel(f"Signed in as: {self.current_user_level}")
        hint.setObjectName("Subtle")
        root.addWidget(hint)

        card = QFrame()
        card.setProperty("class", "Card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(10)

        #only Admin/Super Admin can create accounts
        if self.current_user_level == "Super Admin" or self.current_user_level == "Admin":
            create_btn = QPushButton("Create account")
            create_btn.clicked.connect(self.open_create_account)
            card_layout.addWidget(create_btn)

        theme_btn = QPushButton("Change theme")
        card_layout.addWidget(theme_btn)

        signout_btn = QPushButton("Sign out (Exit)")
        signout_btn.clicked.connect(QApplication.instance().quit)
        card_layout.addWidget(signout_btn)

        root.addWidget(card)

    def open_create_account(self):
        #close settings, then open create account dialog
        self.accept()
        dlg = CreateAccount(accounts_path=self.accounts_path)
        dlg.exec_()

#function to create repeatable card based widgets. layouts of widgets within cards and styles defined
def make_card(title, kpi, caption):
    card = QFrame()
    card.setProperty("class", "Card")

    layout = QVBoxLayout(card)
    layout.setContentsMargins(16, 14, 16, 14)
    layout.setSpacing(6)

    card_title = QLabel(title)
    card_title.setProperty("class", "CardTitle")

    card_num = QLabel(kpi)
    card_num.setProperty("class", "CardKPI")

    card_caption = QLabel(caption)
    card_caption.setProperty("class", "CardCaption")
    card_caption.setWordWrap(True)

    layout.addWidget(card_title)
    layout.addWidget(card_num)
    layout.addWidget(card_caption)
    layout.addStretch(1)
    return card

#function to create repeatable list card based widgets. layouts of widgets within cards and styles defined
def make_reorder_table(title, height=220):
    card = QFrame()
    card.setProperty("class", "Card")

    layout = QVBoxLayout(card)
    layout.setContentsMargins(16, 14, 16, 14)
    layout.setSpacing(10)

    card_title = QLabel(title)
    card_title.setProperty("class", "CardTitle")
    layout.addWidget(card_title)

    demo = [
        ("Record1", 2),
        ("Record2", 0),
        ("Record3", 1),
    ]
    
    table = QTableWidget()
    table.setMinimumHeight(height)
    table.setColumnCount(2)
    table.setHorizontalHeaderLabels(["Item", "Quantity"])
    table.setRowCount(len(demo))

    for x, (name, stock) in enumerate(demo):
        table.setItem(x, 0, QTableWidgetItem(str(name)))
        table.setItem(x, 1, QTableWidgetItem(str(stock)))

    table.setEditTriggers(QTableWidget.NoEditTriggers)
    table.setSelectionBehavior(QTableWidget.SelectRows)
    table.setSelectionMode(QTableWidget.SingleSelection)
    table.setShowGrid(False)
    table.verticalHeader().setVisible(False)

    layout.addWidget(table, 1)
    return card

#function to create repeatable chart card based widgets. layouts of widgets within cards and styles defined
#placeholder until data visuals with Matplotlib are implemented
def make_chart(title, height=220):
    box = QFrame()
    box.setProperty("class", "Card")
    layout = QVBoxLayout(box)
    layout.setContentsMargins(16, 14, 16, 14)
    layout.setSpacing(10)

    card_title = QLabel(title)
    card_title.setProperty("class", "CardTitle")

    chart = QFrame()
    chart.setProperty("class", "ChartBox")
    chart.setMinimumHeight(height)

    inner = QVBoxLayout(chart)
    inner.setContentsMargins(10, 10, 10, 10)
    hint = QLabel("Chart placeholder")
    hint.setObjectName("Subtle")
    hint.setAlignment(Qt.AlignCenter)
    inner.addStretch(1)
    inner.addWidget(hint)
    inner.addStretch(1)

    layout.addWidget(card_title)
    layout.addWidget(chart)
    return box

#initialisation and layout/styles of dashboard tab
class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        header = QHBoxLayout()
        title = QLabel("Page Analytics")
        title.setObjectName("PageTitle")

        sub = QLabel("Overview of inventory, updates and trends.")
        sub.setObjectName("Subtle")

        header_left = QVBoxLayout()
        header_left.setSpacing(3)
        header_left.addWidget(title)
        header_left.addWidget(sub)

        header.addLayout(header_left)
        header.addStretch(1)

        root.addLayout(header)

        #main statistic cards laid out in grid
        grid = QGridLayout()
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(14)

        #KPI card placeholder
        grid.addWidget(make_card("Total Inventory Value", "150", "(£) total"), 0, 0)
        grid.addWidget(make_card("Total Inventory", "20", "items"), 0, 1)
        grid.addWidget(make_card("Total Inventory in Stock", "10", "items"), 0, 2)
        grid.addWidget(make_reorder_table("Reorder List"), 0, 3)
        root.addLayout(grid)

        #bottom row chart placeholder (wide)
        bottom = make_chart("Top 10 Inventory (Quantity)", height=300)
        root.addWidget(bottom)

class ItemCards(QPushButton):
    def __init__(self, name, quantity, price, image_filename):
        super().__init__()
        self.setCursor(Qt.PointingHandCursor)
        self.setProperty("class", "ItemCard")

        self.setFixedSize(240, 220)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(14, 14, 14, 14)
        outer.setSpacing(10)

        #image holder
        self.img_label = QLabel()
        self.img_label.setProperty("class", "ItemImageFrame")
        self.img_label.setFixedHeight(120)
        self.img_label.setAlignment(Qt.AlignCenter)

        #load image from Images/<filename>, show placeholder if error.
        img_path = os.path.join(images_dir(), image_filename or "placeholder.png")
        if not os.path.exists(img_path):
            img_path = os.path.join(images_dir(), "placeholder.png")

        imgPixMap = QPixmap(img_path)
        imgPixMap = imgPixMap.scaled(212, 110, Qt.KeepAspectRatio)
        self.img_label.setPixmap(imgPixMap)

        #text in buttons
        self.name_label = QLabel(name)
        self.name_label.setProperty("class", "ItemName")
        self.name_label.setWordWrap(True)

        self.qty_label = QLabel(f"Quantity: {quantity}")
        self.qty_label.setProperty("class", "ItemQtyPrice")

        self.price_label = QLabel(f"Price: £{price:.2f}")
        self.price_label.setProperty("class", "ItemQtyPrice")

        outer.addWidget(self.img_label)
        outer.addWidget(self.name_label)
        outer.addWidget(self.qty_label)
        outer.addWidget(self.price_label)
        outer.addStretch(1)

#widget that maintains uniform spaced grid. Recalculate columns on resize
class CardGrid(QWidget):
    def __init__(self, card_w, spacing):
        super().__init__()
        self.card_w = card_w
        self.spacing = spacing
        self.cards = []

        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(10, 10, 10, 10)
        self.grid.setHorizontalSpacing(self.spacing)
        self.grid.setVerticalSpacing(self.spacing)
        self.grid.setAlignment(Qt.AlignTop|Qt.AlignLeft)

    def setCards(self, cards):
        #clear existing
        while self.grid.count():
            item = self.grid.takeAt(0)
            fullDelete = item.widget()
            if fullDelete:
                fullDelete.deleteLater()

        self.cards = list(cards)
        self.relayout()
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.relayout()

    def relayout(self):
        #return nothing before errors thrown if no cards
        if not self.cards:
            return

        viewport_w = self.width()
        #calculate how many columns fit
        #max ensures always at least one column
        cols = max(1, (viewport_w + self.spacing) // (self.card_w + self.spacing))

        #re-add cards left to right, then start new row
        for i, cardContent in enumerate(self.cards):
            r = i // cols
            c = i % cols
            self.grid.addWidget(cardContent, r, c)


class ItemsPage(QWidget):
    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        title = QLabel("Items")
        title.setObjectName("PageTitle")
        root.addWidget(title)

        #container for header row (hint+buttons) and scrollable card grid
        panel = QFrame()
        panel.setProperty("class", "Card")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(16, 16, 16, 16)
        panel_layout.setSpacing(12)

        #header row (hint+buttons)
        header_row = QHBoxLayout()
        header_row.setContentsMargins(0, 0, 0, 0)
        header_row.setSpacing(10)

        hint = QLabel("Items within database")
        hint.setObjectName("Subtle")
        header_row.addWidget(hint, 1)
        add_btn = QPushButton("Add Item")
        add_btn.setCursor(Qt.PointingHandCursor)
        header_row.addWidget(add_btn)
        panel_layout.addLayout(header_row)

        #scrollable grid inside panel
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        self.card_grid = CardGrid(card_w=240, spacing=14)
        container_layout.addWidget(self.card_grid, 1)

        scroll.setWidget(container)
        panel_layout.addWidget(scroll, 1)

        root.addWidget(panel, 1)

        #load cards from database
        self.load_cards_from_db()

    #convert SQL entries to cards
    def load_cards_from_db(self):
        query = QSqlQuery()
        query.exec_("SELECT item_id, name, quantity, price, image_path FROM items ORDER BY item_id")

        cards = []
        while query.next():
            name = str(query.value(1))
            quantity = int(query.value(2))
            price = float(query.value(3) or 0)
            image_fn = str(query.value(4) or "placeholder.png") #show placeholder in case image not attached

            card = ItemCards(name=name, quantity=quantity, price=price, image_filename=image_fn)

            cards.append(card)

        self.card_grid.setCards(cards)

class SearchPage(QWidget):
    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        title = QLabel("Search")
        title.setObjectName("PageTitle")

        desc = QLabel("Search items and filter results.")
        desc.setObjectName("Subtle")

        root.addWidget(title)
        root.addWidget(desc)

        #search bar
        top_row = QHBoxLayout()
        self.query = QLineEdit()
        self.query.setPlaceholderText("Search item name...")
        self.search_btn = QPushButton("Search")
        self.search_btn.setCursor(Qt.PointingHandCursor)

        top_row.addWidget(self.query, 1)
        top_row.addWidget(self.search_btn)
        root.addLayout(top_row)

        #main content row
        content_row = QHBoxLayout()
        content_row.setSpacing(14)

        #left filter panel
        filter_card = QFrame()
        filter_card.setProperty("class", "Card")
        filter_card.setFixedWidth(240)

        filter_layout = QVBoxLayout(filter_card)
        filter_layout.setContentsMargins(14, 14, 14, 14)
        filter_layout.setSpacing(12)

        filter_title = QLabel("Filters")
        filter_title.setProperty("class", "CardTitle")
        filter_layout.addWidget(filter_title)

        form = QFormLayout()
        form.setSpacing(10)

        self.qty_min = QSpinBox()
        self.qty_min.setMinimum(0)
        self.qty_min.setMaximum(999)
        self.qty_min.setValue(0)

        self.qty_max = QSpinBox()
        self.qty_max.setMinimum(0)
        self.qty_max.setMaximum(999)
        self.qty_max.setValue(999)

        self.price_min = QDoubleSpinBox()
        self.price_min.setMinimum(0.00)
        self.price_min.setMaximum(999.99)
        self.price_min.setDecimals(2)
        self.price_min.setSingleStep(0.50)
        self.price_min.setValue(0.00)
        self.price_min.setPrefix("£")

        self.price_max = QDoubleSpinBox()
        self.price_max.setMinimum(0.00)
        self.price_max.setMaximum(999.99)
        self.price_max.setDecimals(2)
        self.price_max.setSingleStep(0.50)
        self.price_max.setValue(999.99)
        self.price_max.setPrefix("£")

        self.sort_by = QComboBox()
        self.sort_by.addItems([
            "Name A-Z",
            "Name Z-A",
            "Quantity Low-High",
            "Quantity High-Low",
            "Price Low-High",
            "Price High-Low"
        ])

        form.addRow("Qty min", self.qty_min)
        form.addRow("Qty max", self.qty_max)
        form.addRow("Price min", self.price_min)
        form.addRow("Price max", self.price_max)
        form.addRow("Sort by", self.sort_by)

        filter_layout.addLayout(form)

        self.clear_filters_btn = QPushButton("Clear filters")
        filter_layout.addWidget(self.clear_filters_btn)
        filter_layout.addStretch(1)

        #right results panel
        results_card = QFrame()
        results_card.setProperty("class", "Card")
        results_layout = QVBoxLayout(results_card)
        results_layout.setContentsMargins(16, 16, 16, 16)
        results_layout.setSpacing(12)

        self.results_hint = QLabel("Matching items will appear below.")
        self.results_hint.setObjectName("Subtle")
        results_layout.addWidget(self.results_hint)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        self.card_grid = CardGrid(card_w=240, spacing=14)
        container_layout.addWidget(self.card_grid, 1)

        scroll.setWidget(container)
        results_layout.addWidget(scroll, 1)

        content_row.addWidget(filter_card)
        content_row.addWidget(results_card, 1)

        root.addLayout(content_row, 1)

        #signals when filter changed
        self.query.textChanged.connect(self.apply_filters)
        self.search_btn.clicked.connect(self.apply_filters)

        self.qty_min.valueChanged.connect(self.apply_filters)
        self.qty_max.valueChanged.connect(self.apply_filters)
        self.price_min.valueChanged.connect(self.apply_filters)
        self.price_max.valueChanged.connect(self.apply_filters)
        self.sort_by.currentIndexChanged.connect(self.apply_filters)
        self.clear_filters_btn.clicked.connect(self.clear_filters)

        #initial loading of filters
        self.apply_filters()

    def clear_filters(self):
        self.query.clear()
        self.qty_min.setValue(0)
        self.qty_max.setValue(999)
        self.price_min.setValue(0.00)
        self.price_max.setValue(999.99)
        self.sort_by.setCurrentIndex(0)
        self.apply_filters()

    def apply_filters(self):
        search_text = self.query.text().strip().lower()
        qty_min = self.qty_min.value()
        qty_max = self.qty_max.value()
        price_min = self.price_min.value()
        price_max = self.price_max.value()
        sort_text = self.sort_by.currentText()

        if qty_min > qty_max:
            qty_max = qty_min
            self.qty_max.setValue(qty_max)

        if price_min > price_max:
            price_max = price_min
            self.price_max.setValue(price_max)

        order_command = "name COLLATE NOCASE ASC"
        if sort_text == "Name Z-A":
            order_command = "name COLLATE NOCASE DESC"
        elif sort_text == "Quantity Low-High":
            order_command = "quantity ASC"
        elif sort_text == "Quantity High-Low":
            order_command = "quantity DESC"
        elif sort_text == "Price Low-High":
            order_command = "price ASC"
        elif sort_text == "Price High-Low":
            order_command = "price DESC"

        sql = f"""
            SELECT name, quantity, price, image_path
            FROM items
            WHERE LOWER(name) LIKE ?
              AND quantity BETWEEN ? AND ?
              AND price BETWEEN ? AND ?
            ORDER BY {order_command}
        """

        query = QSqlQuery()
        query.prepare(sql)
        query.addBindValue(f"%{search_text}%") #% wildcard to match any record with part of search_text
        query.addBindValue(qty_min)
        query.addBindValue(qty_max)
        query.addBindValue(price_min)
        query.addBindValue(price_max)
        query.exec_()

        cards = []

        while query.next():
            name = str(query.value(0))
            quantity = int(query.value(1))
            price = float(query.value(2))
            image_fn = str(query.value(3) or "placeholder.png")

            card = ItemCards(name=name, quantity=quantity, price=price, image_filename=image_fn)

            cards.append(card)

        self.card_grid.setCards(cards)
        self.results_hint.setText(f"{len(cards)} matching item(s)")


#initialisation and layout/styles of the main application and everything other than tabs
class MainWindow(QMainWindow):
    def __init__(self, showUsername, showUserlevel):
        super().__init__()
        self.setWindowTitle("TrackStock")
        self.resize(1200, 680)

        #central container
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        #sidebar
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(220)
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(10, 10, 10, 10)
        side_layout.setSpacing(10)

        brand = QLabel("TrackStock")
        brand.setObjectName("Brand")
        side_layout.addWidget(brand)

        self.nav = QListWidget()
        self.nav.setObjectName("NavList")
        self.nav.setSpacing(2)

        for name in ["☰ Dashboard", "❒ Items", "⌕ Search"]:
            QListWidgetItem(name, self.nav)

        self.nav.setCurrentRow(0)
        side_layout.addWidget(self.nav, 1)

        #small footer/profile button
        profile_btn = QPushButton()
        profile_btn.setMinimumHeight(60)
        profile_btn.setObjectName("ProfileFooter")
        profile_btn.setCursor(Qt.PointingHandCursor) #intuitive feature as unclear if is button

        fl = QVBoxLayout(profile_btn)
        fl.setContentsMargins(12, 10, 12, 10)
        fl.setSpacing(3)

        me = QLabel("Signed in")
        me.setProperty("class", "CardTitle")

        hint = QLabel(f"{showUsername} - {showUserlevel}")
        hint.setObjectName("Subtle")

        fl.addWidget(me)
        fl.addWidget(hint)

        side_layout.addWidget(profile_btn)

        #store for settings so knows to show or not account creation
        self.current_user_level = showUserlevel
        
        profile_btn.clicked.connect(self.open_settings)

        #main area
        main = QWidget()
        main_layout = QVBoxLayout(main)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        #use stacked widgets to create different tabs
        self.pages = QStackedWidget()
        self.pages.addWidget(DashboardPage())
        self.pages.addWidget(ItemsPage())
        self.pages.addWidget(SearchPage())

        main_layout.addWidget(self.pages, 1)

        #assemble sidebar and main body
        root.addWidget(sidebar)
        root.addWidget(main, 1)

        #navigation behavior
        self.nav.currentRowChanged.connect(self.pages.setCurrentIndex)

        #set a slightly larger default font for the whole app
        f = QFont()
        f.setPointSize(10)
        QApplication.instance().setFont(f)

    def open_settings(self):
        dlg = Settings(current_user_level=self.current_user_level, accounts_path=ACCOUNTS_PATH)
        dlg.exec_()

#assembling the final result to be run
def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS)

    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName("trackstock.db")
    if not database.open():
        QMessageBox.critical(None, "Database Error", "Could not open trackstock.db")
        sys.exit(0)

    #decide which dialog to show
    if load_accounts(ACCOUNTS_PATH):
        dlg = SignIn(ACCOUNTS_PATH)
        if dlg.exec_() != QDialog.Accepted:
            sys.exit(0)
        username = dlg.signed_in_username
        userlevel = dlg.signed_in_userlevel
    else:
        dlg = InitialAccountCreation(ACCOUNTS_PATH)
        if dlg.exec_() != QDialog.Accepted:
            sys.exit(0)
        username = dlg.created_username
        userlevel = "Super Admin"

    window = MainWindow(showUsername=username, showUserlevel=userlevel)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()