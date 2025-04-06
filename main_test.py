import xlwings as xw

# Biến để lưu trữ dữ liệu đã xử lý
processed_data = {}

def process_cell_value(cell_value):
    # Xử lý dữ liệu (ví dụ: nhân đôi giá trị)
    return cell_value * 2

def main():
    # Kết nối vào Excel
    wb = xw.Book.caller()
    sheet = wb.sheets.active

    # Lấy giá trị từ ô hiện tại
    current_cell = sheet.api.Application.ActiveCell
    cell_value = current_cell.Value

    # Kiểm tra xem giá trị đã được xử lý chưa
    if cell_value in processed_data:
        result = processed_data[cell_value]
    else:
        # Xử lý dữ liệu mới
        result = process_cell_value(cell_value)
        processed_data[cell_value] = result  # Lưu vào biến

    # Trả lại kết quả vào ô
    current_cell.Offset(0, 1).Value = result  # Ghi kết quả vào ô bên phải

@xw.func
def process_selected_cell():
    main()

if __name__ == "__main__":
    main()
