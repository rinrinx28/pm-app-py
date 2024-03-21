from Pages.home import HomePage
from Pages.ngang import NgangPage
from Pages.thong import ThongPage
from Pages.listban import ListBanPage
from Pages.tinh_mau import TinhAndMauPage
class Controller:
    def __init__(self):
        self.current_page = None

    def set_main_widget(self, widget):
        self.main_widget = widget

    def show_home_page(self):
        if self.current_page:
            self.main_widget.layout().removeWidget(self.current_page)
            self.current_page.deleteLater()
        self.current_page = HomePage()
        self.main_widget.layout().addWidget(self.current_page)
    
    def show_ngang_page(self):
        if self.current_page:
            self.main_widget.layout().removeWidget(self.current_page)
            self.current_page.deleteLater()
        self.current_page = NgangPage()
        self.main_widget.layout().addWidget(self.current_page)

    def show_thong_page(self):
        if self.current_page:
            self.main_widget.layout().removeWidget(self.current_page)
            self.current_page.deleteLater()
        self.current_page = ThongPage()
        self.main_widget.layout().addWidget(self.current_page)

    def show_list_ban_page(self):
        if self.current_page:
            self.main_widget.layout().removeWidget(self.current_page)
            self.current_page.deleteLater()
        self.current_page = ListBanPage()
        self.main_widget.layout().addWidget(self.current_page)

    def show_tinh_mau_page(self):
        TinhAndMauPage()