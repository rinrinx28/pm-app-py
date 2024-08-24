from Pages.components.path import Path
from Pages.home import HomePage
from Pages.ngang import NgangPage
from Pages.thong import ThongPage
from Pages.listban import ListBanPage
from Pages.tinh_mau import TinhAndMauPage
from Pages.common.loading import LoadingScreen
from Pages.common.thread import Thread


class Controller:
    def __init__(self, widget):
        super().__init__()
        self.path = Path()
        self.main_widget = widget
        self.current_page = None
        self.loadingScreen = LoadingScreen(self.path.path_loading())

    def show_loading_screen(self):
        self.loadingScreen.show()
        self.loadingScreen.start()

    def hide_loading_screen(self):
        self.loadingScreen.stop()
        self.loadingScreen.hide()

    def show_home_page(self):
        self.show_page(HomePage)

    def show_ngang_page(self):
        self.show_page(NgangPage)

    def show_thong_page(self):
        self.show_page(ThongPage)

    def show_list_ban_page(self):
        self.show_page(ListBanPage)

    def show_tinh_mau_page(self):
        self.show_page(TinhAndMauPage)

    def show_page(self, page_class):
        self.show_loading_screen()
        if self.current_page:
            self.main_widget.layout().removeWidget(self.current_page)
            self.current_page.deleteLater()
            self.current_page = None

        self.thread = Thread()
        self.thread.task_completed.connect(lambda: self.add_page_to_layout(page_class))
        self.thread.start()

    def add_page_to_layout(self, page_class):
        self.hide_loading_screen()
        page = page_class()
        self.current_page = page
        page.show()
