import sys, os, json, hashlib, shutil
from datetime import datetime
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QFrame, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QGridLayout, QListWidget, QListWidgetItem,
    QStackedWidget, QTableWidget, QTableWidgetItem, QDialog, QMessageBox,
    QRadioButton, QScrollArea, QSizePolicy, QComboBox, QFormLayout, QSpinBox,
    QDoubleSpinBox, QTextEdit, QFileDialog
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

/*##########Item Modification##########*/
QTextEdit {
    background: #0b1016;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 9px 12px;
}

QLineEdit:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled, QComboBox:disabled, QTextEdit:disabled {
    background: rgba(255,255,255,0.05);
    color: rgba(215,221,232,0.50);
}

#ImagePreviewFrame {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
}

#ImagePreviewLabel {
    background: transparent;
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

def placeholder_image_path():
    return os.path.join(images_dir(), "placeholder.png")

def load_accounts(path = ACCOUNTS_PATH):
    #return dict of accounts, false if file missing
    if not os.path.exists(path):
        return {}
    else:
        with open(path, "r") as file:
            data = json.load(file)
        return data
    


def isAdmin(user_level):
    return user_level in ("Admin", "Super Admin")

def canSeeItem(user_level, permission_mode):
    if isAdmin(user_level):
        return True
    return permission_mode.strip().lower() != "hidden"

def canEditItem(user_level, permission_mode):
    if isAdmin(user_level):
        return True
    return permission_mode.strip().lower() != "read only"

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

class ItemEditorDialog(QDialog):
    def __init__(self, current_user_level, current_username, item_id=None):
        super().__init__()
        self.current_user_level = current_user_level
        self.current_username = current_username
        self.item_id = item_id
        self.image_filename = None
        self.original_permission_mode = None
        self.initial_state = None

        self.setWindowTitle("Modify Item")
        self.setModal(True)
        self.resize(900, 620)

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        page = QFrame()
        page.setProperty("class", "Card")
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(18, 18, 18, 18)
        page_layout.setSpacing(12)

        content = QHBoxLayout()
        content.setSpacing(20)

        #left side options
        left_col = QVBoxLayout()
        left_col.setSpacing(10)

        title_lbl = QLabel("Item Name")
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter item name")

        self.id_label = QLabel("ID: auto-generated")
        self.id_label.setObjectName("Subtle")

        qty_unit_row = QHBoxLayout()
        qty_unit_row.setSpacing(14)

        qty_box = QVBoxLayout()
        qty_box.addWidget(QLabel("Quantity"))
        self.qty_spin = QSpinBox()
        self.qty_spin.setRange(0, 999)
        qty_box.addWidget(self.qty_spin)

        unit_box = QVBoxLayout()
        unit_box.addWidget(QLabel("Unit"))
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["unit", "kg", "box"])
        unit_box.addWidget(self.unit_combo)

        qty_unit_row.addLayout(qty_box, 1)
        qty_unit_row.addLayout(unit_box, 1)

        price_box = QVBoxLayout()
        price_box.addWidget(QLabel("Price"))
        self.price_spin = QDoubleSpinBox()
        self.price_spin.setRange(0.00, 999.99)
        self.price_spin.setDecimals(2)
        self.price_spin.setSingleStep(0.50)
        price_box.addWidget(self.price_spin)

        low_perm_row = QHBoxLayout()
        low_perm_row.setSpacing(14)

        low_box = QVBoxLayout()
        low_box.addWidget(QLabel("Low Stock"))
        low_inner = QHBoxLayout()
        low_inner.setSpacing(8)

        self.low_threshold_spin = QSpinBox()
        self.low_threshold_spin.setRange(0, 999)
        self.low_threshold_spin.setFixedWidth(90)

        self.low_stock_combo = QComboBox()
        self.low_stock_combo.addItems(["Off", "On"])
        self.low_stock_combo.setFixedWidth(90)

        low_inner.addWidget(self.low_threshold_spin)
        low_inner.addWidget(self.low_stock_combo)
        low_box.addLayout(low_inner)

        perm_box = QVBoxLayout()
        perm_box.addWidget(QLabel("Access level"))
        self.permission_combo = QComboBox()
        self.permission_combo.addItems(["Editable", "Read only", "Hidden"])
        perm_box.addWidget(self.permission_combo)

        low_perm_row.addLayout(low_box)
        low_perm_row.addLayout(perm_box, 1)

        qr_title = QLabel("Generate QR/Barcode")
        qr_row = QHBoxLayout()
        qr_row.setSpacing(10)
        self.qr_btn = QPushButton("QR")
        self.barcode_btn = QPushButton("Barcode")
        qr_row.addWidget(self.qr_btn)
        qr_row.addWidget(self.barcode_btn)

        left_col.addWidget(title_lbl)
        left_col.addWidget(self.name_edit)
        left_col.addWidget(self.id_label)
        left_col.addLayout(qty_unit_row)
        left_col.addLayout(price_box)
        left_col.addLayout(low_perm_row)
        left_col.addWidget(qr_title)
        left_col.addLayout(qr_row)
        left_col.addStretch(1)

        #right side options
        right_col = QVBoxLayout()
        right_col.setSpacing(14)

        self.image_frame = QFrame()
        self.image_frame.setObjectName("ImagePreviewFrame")
        self.image_frame.setMinimumSize(420, 260)
        self.image_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        image_stack = QVBoxLayout(self.image_frame)
        image_stack.setContentsMargins(10, 10, 10, 10)
        image_stack.setSpacing(0)

        self.image_label = QLabel()
        self.image_label.setObjectName("ImagePreviewLabel")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(False)
        self.image_label.setCursor(Qt.PointingHandCursor)
        self.image_label.mousePressEvent = self.image_label_clicked

        self.add_image_btn = QPushButton("Add Image +")
        self.add_image_btn.setFixedSize(160, 42)
        self.add_image_btn.clicked.connect(self.select_image)

        image_stack.addStretch(1)
        image_stack.addWidget(self.image_label, 0, Qt.AlignCenter)
        image_stack.addWidget(self.add_image_btn, 0, Qt.AlignCenter)
        image_stack.addStretch(1)

        notes_title = QLabel("Notes")
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Type here...")
        self.notes_edit.setFixedHeight(140)

        self.modified_label = QLabel("last modified: -")
        self.modified_label.setObjectName("Subtle")

        right_col.addWidget(self.image_frame)
        right_col.addWidget(notes_title)
        right_col.addWidget(self.notes_edit)
        right_col.addWidget(self.modified_label)
        right_col.addStretch(1)

        content.addLayout(left_col, 4)
        content.addLayout(right_col, 6)

        btn_row = QHBoxLayout()

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_item)
        self.delete_btn.setVisible(self.item_id is not None)

        btn_row.addWidget(self.delete_btn)
        btn_row.addStretch(1)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_item)

        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(save_btn)

        page_layout.addLayout(content)
        page_layout.addLayout(btn_row)
        root.addWidget(page)

        self.low_stock_combo.currentTextChanged.connect(self.update_low_stock_state)
        self.update_low_stock_state()

        if self.item_id is not None:
            self.load_item()
        else:
            self.permission_combo.setCurrentText("Editable")

        self.initial_state = self.get_form_state()


    def get_form_state(self):
        return {
            "name": self.name_edit.text().strip(),
            "quantity": self.qty_spin.value(),
            "unit": self.unit_combo.currentText(),
            "price": round(self.price_spin.value(), 2),
            "notes": self.notes_edit.toPlainText().strip(),
            "low_stock": self.low_stock_combo.currentText(),
            "threshold": self.low_threshold_spin.value(),
            "permission_mode": self.permission_combo.currentText(),
            "image_filename": self.image_filename or ""
        }

    def has_unsaved_changes(self):
        return self.get_form_state() != self.initial_state

    def update_low_stock_state(self):
        enabled = self.low_stock_combo.currentText() == "On"
        self.low_threshold_spin.setEnabled(enabled)

    def image_label_clicked(self, event):
        self.select_image()

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select PNG image", "", "PNG Files (*.png)")
        if not file_path:
            return

        filename = os.path.basename(file_path)
        dest_path = os.path.join(images_dir(), filename)

        if os.path.exists(dest_path):
            QMessageBox.warning(self, "Duplicate Image", "An image with this name already exists.")
            return

        shutil.copyfile(file_path, dest_path)

        self.image_filename = filename
        self.show_image_preview(dest_path)

    def show_image_preview(self, full_path):
        pix = QPixmap(full_path)
        scaled = pix.scaled(QSize(390, 230), Qt.KeepAspectRatio)
        self.image_label.setPixmap(scaled)
        self.add_image_btn.hide()

    def load_item(self):
        query = QSqlQuery()
        query.prepare("""
            SELECT item_id, name, quantity, unit, price, notes,
                   low_stock, threshold, permission_mode, image_path, updated
            FROM items
            WHERE item_id = ?
        """)
        query.addBindValue(self.item_id)
        query.exec_()
        query.next()

        item_id = query.value(0)
        name = str(query.value(1) or "")
        quantity = int(query.value(2) or 0)
        unit = str(query.value(3) or "unit")
        price = float(query.value(4) or 0)
        notes = str(query.value(5) or "")
        low_stock = bool(query.value(6))
        threshold = int(query.value(7) or 0)
        permission_mode = str(query.value(8) or "Editable")
        image_path = str(query.value(9) or "")
        updated = str(query.value(10) or "")

        self.id_label.setText(f"ID: {item_id}")
        self.name_edit.setText(name)
        self.qty_spin.setValue(quantity)
        self.unit_combo.setCurrentText(unit)
        self.price_spin.setValue(price)
        self.notes_edit.setPlainText(notes)
        self.low_stock_combo.setCurrentText("On" if low_stock else "Off")
        self.low_threshold_spin.setValue(threshold)
        self.permission_combo.setCurrentText(permission_mode)
        self.original_permission_mode = self.permission_combo.currentText()
        self.modified_label.setText(f"last modified: {updated}" if updated else "last modified: -")

        self.update_low_stock_state()

        self.image_filename = image_path if image_path else None
        if image_path:
            full_path = os.path.join(images_dir(), image_path)
            self.show_image_preview(full_path)


    def confirm_discard_changes(self):
        if not self.has_unsaved_changes():
            return True

        reply = QMessageBox.question(
            self,
            "Unsaved changes",
            "You have unsaved changes. Discard them and close?",
            QMessageBox.Yes | QMessageBox.No
        )
        return reply == QMessageBox.Yes

    def reject(self):
        if self.confirm_discard_changes():
            super().reject()


    def delete_item(self):
        permission_mode_for_check = self.original_permission_mode or self.permission_combo.currentText()
        if not canEditItem(self.current_user_level, permission_mode_for_check):
            QMessageBox.warning(self, "Read only item", "This item is read only. You cannot delete it.")
            return

        reply = QMessageBox.warning(
            self,
            "Delete item",
            "Are you sure you want to delete this item?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        query = QSqlQuery()
        query.prepare("DELETE FROM items WHERE item_id = ?")
        query.addBindValue(self.item_id)

        query.exec_()

        self.accept()

    def save_item(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Missing data", "Please enter an item name.")
            return

        if self.item_id is not None:
            permission_mode_for_check = self.original_permission_mode or self.permission_combo.currentText()
            if not canEditItem(self.current_user_level, permission_mode_for_check):
                QMessageBox.warning(self, "Read only item", "This item is read only. You cannot save changes.")
                return

        quantity = self.qty_spin.value()
        unit = self.unit_combo.currentText()
        price = self.price_spin.value()
        notes = self.notes_edit.toPlainText().strip()
        low_stock_on = self.low_stock_combo.currentText() == "On"
        threshold = self.low_threshold_spin.value() if low_stock_on else 0
        permission_mode = self.permission_combo.currentText()
        updated = datetime.now().strftime(f"{self.current_username}, %d/%m/%y %H:%M")

        query = QSqlQuery()

        if self.item_id is None:
            query.prepare("""
                INSERT INTO items (
                    name, quantity, unit, price, notes,
                    low_stock, threshold, permission_mode, image_path, updated
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """)
            query.addBindValue(name)
            query.addBindValue(quantity)
            query.addBindValue(unit)
            query.addBindValue(price)
            query.addBindValue(notes)
            query.addBindValue(1 if low_stock_on else 0)
            query.addBindValue(threshold)
            query.addBindValue(permission_mode)
            query.addBindValue(self.image_filename)
            query.addBindValue(updated)
            query.exec_()
        else:
            query.prepare("""
                UPDATE items
                SET name = ?, quantity = ?, unit = ?, price = ?, notes = ?,
                    low_stock = ?, threshold = ?, permission_mode = ?, image_path = ?, updated = ?
                WHERE item_id = ?
            """)
            query.addBindValue(name)
            query.addBindValue(quantity)
            query.addBindValue(unit)
            query.addBindValue(price)
            query.addBindValue(notes)
            query.addBindValue(1 if low_stock_on else 0)
            query.addBindValue(threshold)
            query.addBindValue(permission_mode)
            query.addBindValue(self.image_filename)
            query.addBindValue(updated)
            query.addBindValue(self.item_id)
            query.exec_()

        self.accept()

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
    def __init__(self, item_id, name, quantity, price, image_filename):
        super().__init__()
        self.item_id = item_id
        self.setCursor(Qt.PointingHandCursor)
        self.setProperty("class", "ItemCard")

        self.setFixedSize(240, 220)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(14, 14, 14, 14)
        outer.setSpacing(10)

        self.img_label = QLabel()
        self.img_label.setProperty("class", "ItemImageFrame")
        self.img_label.setFixedHeight(120)
        self.img_label.setAlignment(Qt.AlignCenter)

        img_path = os.path.join(images_dir(), image_filename or "placeholder.png")
        if not os.path.exists(img_path):
            img_path = placeholder_image_path()

        imgPixMap = QPixmap(img_path)
        imgPixMap = imgPixMap.scaled(212, 110, Qt.KeepAspectRatio)
        self.img_label.setPixmap(imgPixMap)

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
    def __init__(self, current_user_level, current_username):
        super().__init__()
        self.current_user_level = current_user_level
        self.current_username = current_username

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        title = QLabel("Items")
        title.setObjectName("PageTitle")
        root.addWidget(title)

        panel = QFrame()
        panel.setProperty("class", "Card")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(16, 16, 16, 16)
        panel_layout.setSpacing(12)

        header_row = QHBoxLayout()
        header_row.setContentsMargins(0, 0, 0, 0)
        header_row.setSpacing(10)

        hint = QLabel("Items within database")
        hint.setObjectName("Subtle")
        header_row.addWidget(hint, 1)

        add_btn = QPushButton("Add Item")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self.open_add_item_dialog)
        header_row.addWidget(add_btn)

        panel_layout.addLayout(header_row)

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

        self.load_cards_from_db()

    def open_add_item_dialog(self):
        dlg = ItemEditorDialog(current_user_level=self.current_user_level, current_username=self.current_username)
        if dlg.exec_() == QDialog.Accepted:
            self.load_cards_from_db()

    def open_edit_item_dialog(self, item_id):
        dlg = ItemEditorDialog(current_user_level=self.current_user_level, current_username=self.current_username, item_id=item_id)
        if dlg.exec_() == QDialog.Accepted:
            self.load_cards_from_db()

    def load_cards_from_db(self):
        query = QSqlQuery()
        query.exec_("""
            SELECT item_id, name, quantity, price, image_path, permission_mode
            FROM items
            ORDER BY item_id
        """)

        cards = []
        while query.next():
            item_id = int(query.value(0))
            name = str(query.value(1) or "")
            quantity = int(query.value(2) or 0)
            price = float(query.value(3) or 0)
            image_fn = str(query.value(4) or "placeholder.png")
            permission_mode = str(query.value(5) or "Editable")

            if not canSeeItem(self.current_user_level, permission_mode):
                continue

            card = ItemCards(
                item_id=item_id,
                name=name,
                quantity=quantity,
                price=price,
                image_filename=image_fn
            )
            card.clicked.connect(lambda checked=False, iid=item_id: self.open_edit_item_dialog(iid))
            cards.append(card)

        self.card_grid.setCards(cards)

class SearchPage(QWidget):
    def __init__(self, current_user_level, current_username):
        super().__init__()
        self.current_user_level = current_user_level
        self.current_username = current_username

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        title = QLabel("Search")
        title.setObjectName("PageTitle")

        desc = QLabel("Search items and filter results.")
        desc.setObjectName("Subtle")

        root.addWidget(title)
        root.addWidget(desc)

        top_row = QHBoxLayout()
        self.query = QLineEdit()
        self.query.setPlaceholderText("Search item name...")
        self.search_btn = QPushButton("Search")
        self.search_btn.setCursor(Qt.PointingHandCursor)

        top_row.addWidget(self.query, 1)
        top_row.addWidget(self.search_btn)
        root.addLayout(top_row)

        content_row = QHBoxLayout()
        content_row.setSpacing(14)

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

        self.query.textChanged.connect(self.apply_filters)
        self.search_btn.clicked.connect(self.apply_filters)

        self.qty_min.valueChanged.connect(self.apply_filters)
        self.qty_max.valueChanged.connect(self.apply_filters)
        self.price_min.valueChanged.connect(self.apply_filters)
        self.price_max.valueChanged.connect(self.apply_filters)
        self.sort_by.currentIndexChanged.connect(self.apply_filters)
        self.clear_filters_btn.clicked.connect(self.clear_filters)

        self.apply_filters()

    def open_edit_item_dialog(self, item_id):
        dlg = ItemEditorDialog(current_user_level=self.current_user_level, current_username=self.current_username, item_id=item_id)
        if dlg.exec_() == QDialog.Accepted:
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
            SELECT item_id, name, quantity, price, image_path, permission_mode
            FROM items
            WHERE LOWER(name) LIKE ?
              AND quantity BETWEEN ? AND ?
              AND price BETWEEN ? AND ?
            ORDER BY {order_command}
        """

        query = QSqlQuery()
        query.prepare(sql)
        query.addBindValue(f"%{search_text}%")
        query.addBindValue(qty_min)
        query.addBindValue(qty_max)
        query.addBindValue(price_min)
        query.addBindValue(price_max)
        query.exec_()

        cards = []

        while query.next():
            item_id = int(query.value(0))
            name = str(query.value(1) or "")
            quantity = int(query.value(2) or 0)
            price = float(query.value(3) or 0)
            image_fn = str(query.value(4) or "placeholder.png")
            permission_mode = str(query.value(5) or "Editable")

            if not canSeeItem(self.current_user_level, permission_mode):
                continue

            card = ItemCards(
                item_id=item_id,
                name=name,
                quantity=quantity,
                price=price,
                image_filename=image_fn
            )
            card.clicked.connect(lambda checked=False, iid=item_id: self.open_edit_item_dialog(iid))
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
        #store username for audit trail
        self.current_username = showUsername
        
        profile_btn.clicked.connect(self.open_settings)

        #main area
        main = QWidget()
        main_layout = QVBoxLayout(main)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.pages = QStackedWidget()
        self.dashboard_page = DashboardPage()
        self.items_page = ItemsPage(current_user_level=showUserlevel, current_username=showUsername)
        self.search_page = SearchPage(current_user_level=showUserlevel, current_username=showUsername)

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.items_page)
        self.pages.addWidget(self.search_page)

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