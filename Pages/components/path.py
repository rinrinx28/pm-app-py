import os


class Path:

    def __init__(self):
        super().__init__()
        check_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "../..", "path_file.txt"
        )
        with open(check_path) as file:
            path_automatic = file.read()

        self.current_dir = path_automatic  # / File Data for Windows

    def path_logo(self):
        path = os.path.join(self.current_dir, "image", "logo.ico")
        return path

    def path_loading(self):
        path = os.path.join(self.current_dir, "image", "loading.gif")
        return path

    def path_wel(self):
        path = os.path.join(self.current_dir, "image", "horse.jpg")
        return path

    def path_thong(self):
        path = os.path.join(self.current_dir, "thong")
        return path

    def path_thong_with_id_value(self, id, value):
        thong_path = self.path_thong()
        path = os.path.join(thong_path, f"thong_{id}_{value}.json")
        return path

    def path_number(self):
        path = os.path.join(self.current_dir, "number")
        return path

    def path_number_with_value(self, value):
        number_path = self.path_number()
        path = os.path.join(number_path, f"number_{value}.json")
        return path

    def path_db(self):
        path = os.path.join(self.current_dir, "db", "index.json")
        return path
