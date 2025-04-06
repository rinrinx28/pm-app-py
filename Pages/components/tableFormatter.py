class TableFormatter:
    def __init__(self, sheet):
        self.sheet = sheet
        self.sheet.select()
        self.sheet.activate()
        
        # Xác định phạm vi bảng (tự động tìm kích thước bảng)
        last_row = self.sheet.range("A1").end("down").row
        last_col = self.sheet.range("A1").end("right").column
        table_range = self.sheet.range((1, 1), (last_row, last_col))

        # 🌟 **Áp dụng định dạng cho toàn bảng**
        table_range.api.Font.Name = "Arial"  # Font chữ
        table_range.api.Font.Size = 24  # Cỡ chữ
        table_range.api.HorizontalAlignment = -4108  # Căn giữa
        table_range.api.VerticalAlignment = -4107  # Căn giữa theo chiều dọc
        table_range.api.Borders.Weight = 2  # Độ dày đường viền
        table_range.api.Font.Bold = True  # In đậm tiêu đề
        table_range.api.NumberFormat = "@"
        
    def apply_formats(self, headers, format_rules):

        # 1. Xử lý headers có chữ "T."
        for i, header in enumerate(headers[0]):
            if "T." in header:
                col_name = self.get_column_name(i + 1)
                self.sheet.range(f"{col_name}:{col_name}").font.color = (255, 0, 0)
        
        # 2. Tạo dictionary để nhóm các cells theo vị trí gần nhau
        font_color_groups = {}  # {(color, row): [cols]}
        background_color_groups = {}  # {(color, row): [cols]}
        
        # Nhóm các cells theo row và color
        for rule in format_rules:
            row = rule["row"]
            col = rule["col"]
            
            if rule.get("color"):
                color_key = (tuple(rule["color"]) if isinstance(rule["color"], list) else rule["color"], row)
                if color_key not in font_color_groups:
                    font_color_groups[color_key] = []
                font_color_groups[color_key].append(col)
            
            if rule.get("notice"):
                notice_key = (tuple(rule["notice"]) if isinstance(rule["notice"], list) else rule["notice"], row)
                if notice_key not in background_color_groups:
                    background_color_groups[notice_key] = []
                background_color_groups[notice_key].append(col)
        
        # 3. Áp dụng định dạng cho từng nhóm cells liền kề
        for (color, row), cols in font_color_groups.items():
            # Sắp xếp các cột
            cols.sort()
            
            # Tạo ranges cho các cột liền kề
            ranges = []
            start_col = cols[0]
            prev_col = start_col
            
            for col in cols[1:] + [None]:
                if col is None or col != prev_col + 1:
                    # Tạo range cho nhóm cột liền kề
                    start_cell = f"{self.get_column_name(start_col)}{row}"
                    end_cell = f"{self.get_column_name(prev_col)}{row}"
                    ranges.append(f"{start_cell}:{end_cell}")
                    if col is not None:
                        start_col = col
                prev_col = col if col is not None else prev_col
            
            # Áp dụng định dạng cho từng range
            for range_str in ranges:
                self.sheet.range(range_str).font.color = color
        
        # 4. Tương tự cho background color
        for (color, row), cols in background_color_groups.items():
            cols.sort()
            ranges = []
            start_col = cols[0]
            prev_col = start_col
            
            for col in cols[1:] + [None]:
                if col is None or col != prev_col + 1:
                    start_cell = f"{self.get_column_name(start_col)}{row}"
                    end_cell = f"{self.get_column_name(prev_col)}{row}"
                    ranges.append(f"{start_cell}:{end_cell}")
                    if col is not None:
                        start_col = col
                prev_col = col if col is not None else prev_col
            
            for range_str in ranges:
                self.sheet.range(range_str).color = color

        self.sheet.autofit('c')  # 'c' để autofit các cột
    
    @staticmethod
    def get_column_name(col_num):
        """Chuyển đổi số cột thành tên cột Excel (A, B, C, ..., AA, AB, ...)"""
        result = ""
        while col_num > 0:
            col_num -= 1
            result = chr(col_num % 26 + 65) + result
            col_num //= 26
        return result