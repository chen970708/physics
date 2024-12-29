import tkinter as tk
from tkinter import messagebox
import pygame
import numpy as np

# 預設物理參數
size = 10              # 小球半徑
v0 = 50                # 小球初速 (預設為50)
theta = np.radians(30) # 小球拋射角度
g = 9.8                # 重力加速度
dt = 0.01              # 更小的時間間隔
screen_width = 400     # 視窗寬度
screen_height = 300    # 視窗高度


# 小球顏色設定
ball_color = (255, 0, 0)  # 小球顏色：紅色
trail_color = (100, 100, 255)  # 軌跡顏色：藍色

# 定義全局變數來存儲用戶輸入的參數
radius_entry = None
speed_entry = None
angle_entry = None
gravity_entry = None
air_resistance_coeff_entry = None
air_resistance_coeff = 0
# 存儲軌跡的位置
trail_positions = []
simulation_mode = 1  # 預設模式為斜向拋射（1: 斜向拋射, 2: 水平拋射）

# 驗證輸入參數
def validate_input():
    global size, v0, theta, g
    try:
        size = int(radius_entry.get())
        v0 = float(speed_entry.get())
        theta = np.radians(float(angle_entry.get()))
        g = float(gravity_entry.get())
        if size <= 0 or v0 <= 0 or g <= 0:
            raise ValueError("參數必須為正數")
    except ValueError as e:
        messagebox.showerror("輸入錯誤", f"無效的輸入: {e}")
        return False
    return True

# 清除軌跡的函數
def clear_trail():
    global trail_positions
    trail_positions.clear()  # 清除軌跡資料
    screen.fill((255, 255, 255))  # 清空畫面
    draw_grid()  # 繪製網格
    pygame.display.flip()  # 即時更新畫面
    print("軌跡已清除")

# 繪製小球
def draw_ball(position):
    pygame.draw.circle(screen, ball_color, position.astype(int), size)

# 繪製格線與坐標軸
def draw_grid():
    grid_color = (200, 200, 200)  # 格線顏色
    for x in range(0, screen_width, 50):
        pygame.draw.line(screen, grid_color, (x, 0), (x, screen_height))
    for y in range(0, screen_height, 50):
        pygame.draw.line(screen, grid_color, (0, y), (screen_width, y))

# 設定模擬循環
def run_physics_simulation():
    global screen, trail_positions, simulation_mode, air_resistance_coeff
    try:
        air_resistance_coeff = float(air_resistance_coeff_entry.get())
    except ValueError:
        air_resistance_coeff = 0  # 預設空氣阻力為 0（無空氣阻力）
    # 初始化小球的位置和速度
    if simulation_mode == 1:  # 斜向拋射
        ball_pos = np.array([screen_width / 4, screen_height - size])  # 初始位置
        ball_vel = np.array([v0 * np.cos(theta), -v0 * np.sin(theta)])  # 初始速度
    elif simulation_mode == 2:  # 水平拋射
        ball_pos = np.array([screen_width / 4, 50])  # 初始位置
        ball_vel = np.array([v0, 0])  # 水平方向初始速度

    clock = pygame.time.Clock()

    # 加入支援中文的字型
    try:
        font_path = "C:/Windows/Fonts/msjh.ttc"  # Windows 微軟正黑體
        font = pygame.font.Font(font_path, 18)
    except FileNotFoundError:
        font = pygame.font.SysFont("SimHei", 18)  # 使用系統內建字體（如 SimHei）

    while True:
        screen.fill((255, 255, 255))
        draw_grid()

        # 繪製軌跡
        for pos in trail_positions:
            pygame.draw.circle(screen, trail_color, pos.astype(int), 1)

        draw_ball(ball_pos)

        # 顯示位置和速度
        position_text = font.render(f"位置: ({ball_pos[0]:.2f}, {ball_pos[1]:.2f})", True, (0, 0, 0))
        velocity_text = font.render(f"速度: ({ball_vel[0]:.2f}, {ball_vel[1]:.2f})", True, (0, 0, 0))
        screen.blit(position_text, (10, 10))
        screen.blit(velocity_text, (10, 40))

        # 計算運動學
        ball_vel[0] -= air_resistance_coeff * ball_vel[0] * dt
        ball_vel[1] += g * dt - air_resistance_coeff * ball_vel[1] * dt

        ball_pos += ball_vel * dt

        # 添加到軌跡
        trail_positions.append(ball_pos.copy())

        # 停止條件
        if ball_pos[1] > screen_height - size:
            #print(f"模擬結束，小球位置: {ball_pos}")
            break

        pygame.display.flip()
        clock.tick(120)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

# 開始模擬
def start_simulation():
    if not validate_input():
        return

    pygame.init()
    global screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("物理模擬")

    run_physics_simulation()

# 顯示參數頁面
def show_parameter_page(page_num):
    global simulation_mode
    simulation_mode = page_num

    for widget in window.winfo_children():
        widget.destroy()

    param_frame = tk.Frame(window, bg="#f0f0f0")
    param_frame.pack(pady=10)

    global radius_entry, speed_entry, angle_entry, gravity_entry, air_resistance_coeff_entry

    tk.Label(param_frame, text="小球半徑 (預設 10):", bg="#f0f0f0").grid(row=0, column=0)
    radius_entry = tk.Entry(param_frame)
    radius_entry.insert(0, "10")
    radius_entry.grid(row=0, column=1)

    tk.Label(param_frame, text="小球初速 (預設 50):", bg="#f0f0f0").grid(row=1, column=0)
    speed_entry = tk.Entry(param_frame)
    speed_entry.insert(0, "50")
    speed_entry.grid(row=1, column=1)

    tk.Label(param_frame, text="拋射角度 (預設 30°):", bg="#f0f0f0").grid(row=2, column=0)
    angle_entry = tk.Entry(param_frame)
    angle_entry.insert(0, "30")
    angle_entry.grid(row=2, column=1)

    tk.Label(param_frame, text="重力加速度 (預設 9.8):", bg="#f0f0f0").grid(row=3, column=0)
    gravity_entry = tk.Entry(param_frame)
    gravity_entry.insert(0, "9.8")
    gravity_entry.grid(row=3, column=1)

    air_resistance_var = tk.BooleanVar()
    tk.Checkbutton(param_frame, text="考慮空氣阻力", variable=air_resistance_var, bg="#f0f0f0").grid(row=4, columnspan=2)

    tk.Label(param_frame, text="空氣阻力係數 (預設 0):").grid(row=4, column=0)
    air_resistance_coeff_entry = tk.Entry(param_frame)
    air_resistance_coeff_entry.insert(0, "0")  # 預設值
    air_resistance_coeff_entry.grid(row=4, column=1)

    tk.Button(window, text="開始模擬", command=start_simulation).pack(pady=20)
    tk.Button(window, text="清除軌跡", command=clear_trail).pack(pady=10)
    tk.Button(window, text="回到首頁", command=show_home_page).pack(side=tk.LEFT, padx=20)
    tk.Button(window, text="結束", command=window.quit).pack(side=tk.RIGHT, padx=10, pady=10)

# 顯示首頁
def show_home_page():
    for widget in window.winfo_children():
        widget.destroy()

    tk.Label(window, text="選擇模擬模式", font=("Arial", 16), bg="#f0f0f0").pack(pady=20)
    tk.Button(window, text="模式 1: 斜向拋射", command=lambda: show_parameter_page(1)).pack(pady=10)
    tk.Button(window, text="模式 2: 水平拋射", command=lambda: show_parameter_page(2)).pack(pady=10)
    tk.Button(window, text="結束", command=window.quit).pack(pady=20)

# 主介面設置
window = tk.Tk()
window.title("拋體運動模擬")
window.configure(bg="#f0f0f0")
window.geometry("400x400")
show_home_page()
window.mainloop()
