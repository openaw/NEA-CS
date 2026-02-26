import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QFrame, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QGridLayout, QListWidget, QListWidgetItem,
    QStackedWidget, QTableWidget, QTableWidgetItem, QHeaderView
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
    padding: 0px;
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
"""

#function to create repeatable card based widgets. layouts of widgets within cards and styles defined
def make_card(title: str, kpi: str, caption: str):
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
def make_reorder_table(title: str, height: int = 220):
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
def make_chart(title: str, height: int = 220):
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

#initialisation and layout/styles of items tab
class ItemsPage(QWidget):
    def __init__(self):
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        title = QLabel("Items")
        title.setObjectName("PageTitle")
        root.addWidget(title)

        panel = QFrame()
        panel.setProperty("class", "Card")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        hint = QLabel("A simple list.")
        hint.setObjectName("Subtle")

        layout.addWidget(hint)

        actions = QHBoxLayout()
        actions.addStretch(1)
        actions.addWidget(QPushButton("Add Item"))
        actions.addWidget(QPushButton("Remove"))
        layout.addLayout(actions)

        root.addWidget(panel, 1)

#initialisation and layout/styles of search tab
class SearchPage(QWidget):
    def __init__(self):
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        title = QLabel("Search")
        title.setObjectName("PageTitle")

        desc = QLabel("A search layout with results panel.")
        desc.setObjectName("Subtle")

        root.addWidget(title)
        root.addWidget(desc)

        row = QHBoxLayout()
        self.query = QLineEdit()
        self.query.setPlaceholderText("Search items, pages, or users…")
        btn = QPushButton("Search")

        row.addWidget(self.query, 1)
        row.addWidget(btn)
        root.addLayout(row)

        results = QFrame()
        results.setProperty("class", "Card")
        layout = QVBoxLayout(results)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        lab = QLabel("Results")
        lab.setProperty("class", "CardTitle")


#initialisation and layout/styles of the main application and everything other than tabs
class MainWindow(QMainWindow):
    def __init__(self):
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

        # small footer/profile button
        profile_btn = QPushButton()
        profile_btn.setMinimumHeight(60)
        profile_btn.setObjectName("ProfileFooter")
        profile_btn.setCursor(Qt.PointingHandCursor) #Intuitive feature as unclear if is button

        fl = QVBoxLayout(profile_btn)
        fl.setContentsMargins(12, 10, 12, 10)
        fl.setSpacing(3)

        me = QLabel("Signed in")
        me.setProperty("class", "CardTitle")

        hint = QLabel("Account123")
        hint.setObjectName("Subtle")

        fl.addWidget(me)
        fl.addWidget(hint)

        side_layout.addWidget(profile_btn)

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

#assembling the final result to be run
def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
