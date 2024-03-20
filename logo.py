import os
class Logo():
    def __init__(self):
        super().__init__()
    def getLogo(self):
        file_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(file_dir, 'logo.png')
        return file_path