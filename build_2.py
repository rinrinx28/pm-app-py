import subprocess
import shutil
import os


def run_command(command):
    """Chạy lệnh và chờ nó hoàn thành."""
    result = subprocess.run(command, shell=True)
    return result.returncode


def move_files_and_dirs(source_paths, destination_dir):
    """Di chuyển các thư mục và file chỉ định tới thư mục mới."""
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    for path in source_paths:
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.move(path, os.path.join(destination_dir, os.path.basename(path)))
            elif os.path.isfile(path):
                shutil.move(path, destination_dir)


if __name__ == "__main__":
    # Đọc lệnh từ package.json
    command = "npm run build"

    # Chỉ định các thư mục và file cần di chuyển
    current_dir = os.path.dirname(os.path.abspath(__file__))
    files_and_dirs_to_move = [f"{current_dir}/dist", f"{current_dir}/build"]
    destination_directory = "D:\Dulieu\Javascript-Project\Frelance\package\App_All"
    # Kiểm tra cách thư mục build và xóa
    for file in files_and_dirs_to_move:
        if os.path.exists(file):
            shutil.rmtree(file)
    app_v = 3

    # for v in range(app_v):
    for c in range(1):
        count = 90
        new_app_file = os.path.join(destination_directory, f"{count}")
        if os.path.exists(new_app_file):
            shutil.rmtree(new_app_file)

        os.makedirs(new_app_file, exist_ok=True)
        # Change Path Data for Application
        path_data = os.path.join(current_dir, "path_file.txt")
        with open(path_data, "r") as file:
            data_file = file.read()

        data_file_arr = data_file.split("/")
        data_file_arr[len(data_file_arr) - 1] = f"{count}"
        data_file_new = "/".join(data_file_arr)
        with open(path_data, "w", encoding="utf-8") as file:
            file.write(data_file_new)

        # Running Command
        print("Running command:", command)
        return_code = run_command(command)

        if return_code == 0:
            print("Command completed successfully.")

            # Di chuyển các file và thư mục
            move_files_and_dirs(files_and_dirs_to_move, new_app_file)

            print(f"Files and directories moved successfully. App {count}")
        else:
            print("Command failed with return code:", return_code)
