import os
class Path():
    
    def __init__(self):
        super().__init__()
        self.current_dir = fr'C:\data\25' #/ File Data for Windows
        # self.current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..','..','data') #/ File Data for Dev
    def path_logo(self):
        path = os.path.join(self.current_dir,'image','logo.ico')
        return path
    def path_wel(self):
        path = os.path.join(self.current_dir,'image','horse.jpg')
        return path
    def path_thong(self):
        path = os.path.join(self.current_dir,'thong')
        return path
    def path_thong_with_id_value(self, id, value):
        thong_path = self.path_thong()
        path = os.path.join(thong_path, f'thong_{id}_{value}.json')
        return path
    def path_number(self):
        path = os.path.join(self.current_dir,'number')
        return path
    def path_number_with_value(self, value):
        number_path = self.path_number()
        path = os.path.join(number_path, f'number_{value}.json')
        return path
    def path_db(self):
        path = os.path.join(self.current_dir, 'db','index.json')
        return path