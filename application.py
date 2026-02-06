import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QFrame, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QGridLayout, QListWidget, QListWidgetItem,
    QStackedWidget
)

QSS = """

/* overall general theme */

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

/*##########Placeholder charts##########*/
.ChartBox {
    background: rgba(11,16,22,0.65);
    border: 1px dashed rgba(255,255,255,0.10);
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
"""

#function to create repeatable card based widgets. layouts of widgets within cards and styles defined
def make_card(title: str, kpi: str, caption: str):
    card = QFrame()
    card.setProperty("class", "Card")
    card.setObjectName("Card")

    layout = QVBoxLayout(card)
    layout.setContentsMargins(16, 14, 16, 14)
    layout.setSpacing(6)

    card_title = QLabel(title)
    card_title.setProperty("class", "CardTitle")
    card_title.setObjectName("CardTitle")

    card_num = QLabel(kpi)
    card_num.setProperty("class", "CardKPI")
    card_num.setObjectName("CardKPI")

    card_caption = QLabel(caption)
    card_caption.setProperty("class", "CardCaption")
    card_caption.setObjectName("CardCaption")
    card_caption.setWordWrap(True)

    layout.addWidget(card_title)
    layout.addWidget(card_num)
    layout.addWidget(card_caption)
    layout.addStretch(1)
    return card

#function to create repeatable chart card based widgets. layouts of widgets within cards and styles defined
#placeholder until data visuals with Matplotlib are implemented
def make_chart_placeholder(title: str, height: int = 220):
    box = QFrame()
    box.setProperty("class", "Card")
    lay = QVBoxLayout(box)
    lay.setContentsMargins(16, 14, 16, 14)
    lay.setSpacing(10)

    card_title = QLabel(title)
    card_title.setProperty("class", "CardTitle")
    card_title.setObjectName("CardTitle")

    chart = QFrame()
    chart.setProperty("class", "ChartBox")
    chart.setMinimumHeight(height)

    inner = QVBoxLayout(chart)
    inner.setContentsMargins(10, 10, 10, 10)
    hint = QLabel("Chart placeholder")
    hint.setObjectName("Subtle")
    hint.setProperty("class", "Subtle")
    hint.setAlignment(Qt.AlignCenter)
    inner.addStretch(1)
    inner.addWidget(hint)
    inner.addStretch(1)

    lay.addWidget(card_title)
    lay.addWidget(chart)
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
        title.setProperty("class", "PageTitle")

        sub = QLabel("Overview of inventory, updates and trends.")
        sub.setObjectName("Subtle")
        sub.setProperty("class", "Subtle")

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

        #top KPI card placeholder
        grid.addWidget(make_card("Incoming Inventory", "150", "New Items Added\nOver the last month you got 150 new stocks added."), 0, 0)

        #top chart placeholder (single)
        main_chart = make_chart_placeholder("Incoming and Outgoing Chart", height=260)
        grid.addWidget(main_chart, 0, 1, 1, 2)

        #middle row card placeholder
        grid.addWidget(make_chart_placeholder("Sales today", height=200), 1, 0)

        #middle row product category placeholders
        grid.addWidget(make_chart_placeholder("Incoming", height=200), 1, 1)
        grid.addWidget(make_chart_placeholder("Outgoing", height=200), 1, 2)

        root.addLayout(grid)

        #bottom row chart placeholder (wide)
        bottom = make_chart_placeholder("Top Outgoing Sources", height=180)
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
        title.setProperty("class", "PageTitle")
        root.addWidget(title)

        panel = QFrame()
        panel.setProperty("class", "Card")
        lay = QVBoxLayout(panel)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(10)

        hint = QLabel("A simple list.")
        hint.setObjectName("Subtle")
        hint.setProperty("class", "Subtle")

        lay.addWidget(hint)

        #custom list design as unique
        list_items = QListWidget()
        list_items.setStyleSheet("""
            QListWidget {
                background: #0b1016;
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 12px;
                padding: 6px;
            }
            QListWidget::item {
                padding: 10px 10px;
                margin: 4px;
                border-radius: 10px;
            }
            QListWidget::item:hover { background: rgba(255,255,255,0.05); }
            QListWidget::item:selected {
                background: rgba(118,142,255,0.18);
                border: 1px solid rgba(118,142,255,0.25);
            }
        """)

        for i in range(1, 13):
            QListWidgetItem(f"Item #{i}  •  status: active  •  updated: today", list_items)

        lay.addWidget(list_items, 1)

        actions = QHBoxLayout()
        actions.addStretch(1)
        actions.addWidget(QPushButton("Add Item"))
        actions.addWidget(QPushButton("Remove"))
        lay.addLayout(actions)

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
        title.setProperty("class", "PageTitle")

        desc = QLabel("A search layout with results panel.")
        desc.setObjectName("Subtle")
        desc.setProperty("class", "Subtle")

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
        lay = QVBoxLayout(results)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(10)

        lab = QLabel("Results")
        lab.setProperty("class", "CardTitle")
        lab.setObjectName("CardTitle")

        #custom list design as unique
        self.results_list = QListWidget()
        self.results_list.setStyleSheet("""
            QListWidget {
                background: #0b1016;
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 12px;
                padding: 6px;
            }
            QListWidget::item {
                padding: 10px 10px;
                margin: 4px;
                border-radius: 10px;
            }
            QListWidget::item:hover { background: rgba(255,255,255,0.05); }
        """)

        lay.addWidget(lab)
        lay.addWidget(self.results_list, 1)
        root.addWidget(results, 1)

        #placeholder function for searching items in list
        def do_search():
            q = self.query.text().strip()
            self.results_list.clear()
            if not q:
                QListWidgetItem("Type something to search.", self.results_list)
                return
            for i in range(1, 6):
                QListWidgetItem(f"Result {i} for “{q}”", self.results_list)

        btn.clicked.connect(do_search)
        self.query.returnPressed.connect(do_search)


#initialisation and layout/styles of the main application and everything other than tabs
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TrackStock")
        self.resize(1100, 680)

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
        self.nav.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.nav.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for name in ["☰ Dashboard", "❒ Items", "⌕ Search"]:
            QListWidgetItem(name, self.nav)

        self.nav.setCurrentRow(0)
        side_layout.addWidget(self.nav, 1)

        #small footer/profile placeholder
        footer = QFrame()
        footer.setProperty("class", "Card")
        fl = QVBoxLayout(footer)
        fl.setContentsMargins(12, 10, 12, 10)
        fl.setSpacing(3)
        me = QLabel("Signed in")
        me.setProperty("class", "CardTitle")
        me.setObjectName("CardTitle")
        hint = QLabel("you@example.com")
        hint.setObjectName("Subtle")
        hint.setProperty("class", "Subtle")
        fl.addWidget(me)
        fl.addWidget(hint)
        side_layout.addWidget(footer)

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
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()