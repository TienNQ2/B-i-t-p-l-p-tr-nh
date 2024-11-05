import tkinter as tk
from tkinter import filedialog, messagebox
import re
import csv


# Hàm đọc file ip-chan.txt để lấy danh sách ID ứng dụng bị chặn
def extract_blocked_apps(file_path):
    blocked_apps = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if 'comment' in line:
                    match = re.search(r'app_(\d+)', line)
                    if match:
                        app_id = match.group(1)
                        blocked_apps.append(app_id)
    except Exception as e:
        messagebox.showerror("Error", f"Could not read ip-chan file: {e}")
    return blocked_apps

# Hàm loại bỏ các ID ứng dụng bị trùng lặp
def list_unique_apps(blocked_apps):
    return list(dict.fromkeys(blocked_apps))

# Hàm đọc App_ID.csv để lấy từ điển ID ứng dụng và tên ứng dụng
def read_app_id(file_path):
    app_dict = {}
    try:
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                app_dict[row['App ID']] = row['app_name']
    except Exception as e:
        messagebox.showerror("Error", f"Could not read App_ID file: {e}")
    return app_dict

# Hàm xử lý sau khi người dùng chọn file và nhấn nút thực hiện
def process_files():
    if not ip_chan_file or not app_id_file:
        messagebox.showwarning("Warning", "Please select both ip-chan.txt and App_ID.csv files.")
        return

    blocked_apps = extract_blocked_apps(ip_chan_file)
    unique_blocked_apps = list_unique_apps(blocked_apps)
    app_dict = read_app_id(app_id_file)

    blocked_app_names = [app_dict[app_id] for app_id in unique_blocked_apps if app_id in app_dict]

    if blocked_app_names:
        result_text.set("\n".join(blocked_app_names))
    else:
        result_text.set("No blocked applications found.")

# Hàm để chọn file ip-chan.txt
def browse_ip_chan():
    global ip_chan_file
    ip_chan_file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    ip_chan_label.config(text=f"Selected: {ip_chan_file}")

# Hàm để chọn file App_ID.csv
def browse_app_id():
    global app_id_file
    app_id_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    app_id_label.config(text=f"Selected: {app_id_file}")

# Hàm để lưu kết quả vào file blocked_apps.txt
from tkinter import filedialog

def save_results():
    # Hiển thị hộp thoại để người dùng chọn tên file và vị trí lưu
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",  # Đặt đuôi mặc định là .txt
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        title="Save results as"  # Tiêu đề của hộp thoại
    )

    # Kiểm tra nếu người dùng không hủy hộp thoại
    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(result_text.get())
            messagebox.showinfo("Success", f"Results saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")


# Giao diện Tkinter
root = tk.Tk()
root.title("Application Block Checker")

# Biến lưu trữ đường dẫn file và kết quả hiển thị
ip_chan_file = None
app_id_file = None
result_text = tk.StringVar()

# Label và nút chọn file ip-chan.txt
ip_chan_label = tk.Label(root, text="Select ip-chan.txt file")
ip_chan_label.pack(pady=5)
ip_chan_button = tk.Button(root, text="Browse", command=browse_ip_chan)
ip_chan_button.pack()

# Label và nút chọn file App_ID.csv
app_id_label = tk.Label(root, text="Select App_ID.csv file")
app_id_label.pack(pady=5)
app_id_button = tk.Button(root, text="Browse", command=browse_app_id)
app_id_button.pack()

# Nút xử lý
process_button = tk.Button(root, text="Process", command=process_files)
process_button.pack(pady=10)

# Kết quả
result_label = tk.Label(root, text="Blocked applications:")
result_label.pack()
result_display = tk.Label(root, textvariable=result_text, fg="blue")
result_display.pack()

# Nút lưu kết quả
save_button = tk.Button(root, text="Save Results", command=save_results)
save_button.pack(pady=5)

# Bắt đầu vòng lặp giao diện Tkinter
root.mainloop()
