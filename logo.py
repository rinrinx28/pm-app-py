import os
class Logo():
    def __init__(self):
        super().__init__()
    def getLogo(self):
        file_dir = fr'C:\data'
        file_path = os.path.join(file_dir, 'logo.png')
        return file_path