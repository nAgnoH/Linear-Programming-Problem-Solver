import tkinter as tk
from scipy.optimize import linprog
import numpy as np

def solve_linear_program():
    num_variables = int(variables_entry.get())
    objective_type = objective_var.get()

    if objective_type == "min":
        c = list(map(float, objective_coeffs_entry.get().split()))
    elif objective_type == "max":
        c_input = objective_coeffs_entry.get()
        c = [-float(coeff) for coeff in c_input.split()]
    else:
        result_label.config(text="Hãy chọn min hoặc max.")
        return

    num_constraints = int(constraints_entry.get())
    constraint_coeffs = []
    constraint_rhs = []

    for i in range(num_constraints):
        constraint_input = constraint_coeffs_entries[i].get()
        condition = constraint_conditions[i].get()

        if condition == ">=":
            coeffs = list(map(float, constraint_input.split()))
            negative_coeffs = [-x for x in coeffs]
            constraint_coeffs.append(negative_coeffs)
            rhs = float(constraint_rhs_entries[i].get())
            constraint_rhs.append(-rhs)
        elif condition == "=":
            coeffs1 = list(map(float, constraint_input.split()))
            constraint_coeffs.append(coeffs1)
            rhs = float(constraint_rhs_entries[i].get())
            constraint_rhs.append(rhs)
            coeffs2 = [-x for x in coeffs1]
            constraint_coeffs.append(coeffs2)
            constraint_rhs.append(-rhs)
        else:
            coeffs = list(map(float, constraint_input.split()))
            constraint_coeffs.append(coeffs)
            rhs = float(constraint_rhs_entries[i].get())
            constraint_rhs.append(rhs)

    x_bounds = []
    for i in range(num_variables):
        lower_bound = float(bounds_entries[i][0].get())
        upper_bound = float(bounds_entries[i][1].get())
        x_bounds.append((lower_bound, upper_bound))

    result = linprog(c, A_ub=constraint_coeffs, b_ub=constraint_rhs, bounds=x_bounds)

    if result.success:
        if objective_type == 'max':
            result_label.config(text="Giá trị tối ưu: " + str(round(-result.fun, 3)))
        else:
            result_label.config(text="Giá trị tối ưu: " + str(round(result.fun, 3)))
        result_variables_label.config(text="Giá trị biến tối ưu: " + str(np.round(result.x, 2)))
    else:
        result_label.config(text="Không tìm thấy giải pháp tối ưu.")

def reset():
    # Xóa dữ liệu cũ
    for widget in constraint_frame.winfo_children():
        widget.destroy()
    for widget in bounds_frame.winfo_children():
        widget.destroy()

    # Cập nhật biến
    constraint_coeffs_entries.clear()
    constraint_rhs_entries.clear()
    constraint_conditions.clear()
    bounds_entries.clear()

    # Reset các entry và label
    variables_entry.delete(0, tk.END)
    objective_coeffs_entry.delete(0, tk.END)
    constraints_entry.delete(0, tk.END)
    objective_var.set("min")
    result_label.config(text="")
    result_variables_label.config(text="")

# Tạo cửa sổ giao diện
window = tk.Tk()
window.title("Giải bài toán quy hoạch tuyến tính")

# Khung nhập thông tin
input_frame = tk.Frame(window)
input_frame.pack(pady=10)

variables_label = tk.Label(input_frame, text="Số lượng biến:")
variables_label.grid(row=0, column=0, padx=5)
variables_entry = tk.Entry(input_frame)
variables_entry.grid(row=0, column=1, padx=5)

objective_label = tk.Label(input_frame, text="Hàm mục tiêu:")
objective_label.grid(row=1, column=0, padx=5)
objective_var = tk.StringVar()
objective_var.set("min")
objective_menu = tk.OptionMenu(input_frame, objective_var, "min", "max")
objective_menu.grid(row=1, column=1, padx=5)

objective_coeffs_label = tk.Label(input_frame, text="Hệ số hàm mục tiêu:")
objective_coeffs_label.grid(row=2, column=0, padx=5)
objective_coeffs_entry = tk.Entry(input_frame)
objective_coeffs_entry.grid(row=2, column=1, padx=5)

constraints_label = tk.Label(input_frame, text="Số lượng ràng buộc:")
constraints_label.grid(row=3, column=0, padx=5)
constraints_entry = tk.Entry(input_frame)
constraints_entry.grid(row=3, column=1, padx=5)

create_constraints_button = tk.Button(input_frame, text="Tạo trường nhập liệu", command=lambda: create_constraint_entries())
create_constraints_button.grid(row=3, column=2, padx=5)

constraint_frame = tk.Frame(window)
constraint_frame.pack(pady=10)

bounds_frame = tk.Frame(window)
bounds_frame.pack(pady=10)

solve_button = tk.Button(window, text="Giải", command=solve_linear_program)
solve_button.pack(pady=10)

result_label = tk.Label(window, text="")
result_label.pack()

result_variables_label = tk.Label(window, text="")
result_variables_label.pack()

constraint_coeffs_entries = []
constraint_rhs_entries = []
constraint_conditions = []
bounds_entries = []

# Tạo nút Reset
reset_button = tk.Button(window, text="Reset", command=reset)
reset_button.pack(pady=10)

def create_constraint_entries():
    num_constraints = int(constraints_entry.get())

    for widget in constraint_frame.winfo_children():
        widget.destroy()

    for i in range(num_constraints):
        constraint_label = tk.Label(constraint_frame, text="Ràng buộc " + str(i + 1) + ":")
        constraint_label.grid(row=i, column=0, padx=5, pady=5)

        constraint_coeffs_entry = tk.Entry(constraint_frame)
        constraint_coeffs_entry.grid(row=i, column=1, padx=5, pady=5)
        constraint_coeffs_entries.append(constraint_coeffs_entry)

        condition_var = tk.StringVar()
        condition_var.set(">=")
        condition_menu = tk.OptionMenu(constraint_frame, condition_var, ">=", "<=", "=")
        condition_menu.grid(row=i, column=2, padx=5, pady=5)
        constraint_conditions.append(condition_var)

        constraint_rhs_entry = tk.Entry(constraint_frame)
        constraint_rhs_entry.grid(row=i, column=3, padx=5, pady=5)
        constraint_rhs_entries.append(constraint_rhs_entry)

    num_variables = int(variables_entry.get())

    for widget in bounds_frame.winfo_children():
        widget.destroy()

    for i in range(num_variables):
        bounds_label = tk.Label(bounds_frame, text="Giới hạn biến " + str(i + 1) + ":")
        bounds_label.grid(row=i, column=0, padx=5, pady=5)

        lower_bound_entry = tk.Entry(bounds_frame)
        lower_bound_entry.grid(row=i, column=1, padx=5, pady=5)

        upper_bound_entry = tk.Entry(bounds_frame)
        upper_bound_entry.grid(row=i, column=2, padx=5, pady=5)

        bounds_entries.append((lower_bound_entry, upper_bound_entry))



# Chạy ứng dụng giao diện
window.mainloop()
