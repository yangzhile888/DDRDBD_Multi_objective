import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
import bisect
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 硬编码的设计数据 - 从Excel表格中提取
DESIGN_DATA = {
    'x_values': [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5,
                 10.0],
    'columns': {
        (2.0, 95): [0.0, 0.5, 1.0, 1.2, 1.2, 1.8, 1.8, 2.1, 2.5, 2.8, 3.2, 3.7, 4.2, 4.7, 5.1, 5.5, 6.0, 6.4, 6.8, 7.5,
                    7.9],
        (2.0, 90): [0.0, 0.5, 1.0, 1.5, 1.5, 2.1, 2.3, 2.6, 3.0, 3.4, 3.7, 4.1, 4.4, 4.8, 5.3, 5.7, 6.2, 6.8, 7.2, 7.7,
                    8.1],
        (2.0, 85): [0.0, 0.5, 1.0, 1.5, 1.8, 2.2, 2.4, 2.8, 3.1, 3.5, 3.8, 4.2, 4.5, 5.0, 5.4, 5.9, 6.4, 6.9, 7.3, 7.8,
                    8.2],
        (2.0, 80): [0.0, 0.5, 1.0, 1.5, 2.0, 2.2, 2.5, 2.9, 3.2, 3.5, 3.9, 4.3, 4.6, 5.1, 5.5, 6.0, 6.5, 7.0, 7.4, 7.9,
                    8.3],
        (2.0, 70): [0.0, 0.5, 1.0, 1.5, 2.0, 2.3, 2.6, 3.0, 3.4, 3.7, 4.0, 4.4, 4.9, 5.3, 5.8, 6.3, 6.7, 7.2, 7.6, 8.1,
                    8.6],
        (2.0, 60): [0.0, 0.5, 1.0, 1.5, 2.0, 2.4, 2.7, 3.1, 3.5, 3.8, 4.2, 4.6, 5.1, 5.6, 6.0, 6.4, 6.9, 7.4, 7.9, 8.4,
                    8.9],
        (2.0, 50): [0.0, 0.5, 1.0, 1.5, 2.0, 2.4, 2.7, 3.1, 3.5, 3.9, 4.3, 4.9, 5.4, 5.7, 6.1, 6.7, 7.2, 7.7, 8.2, 8.7,
                    9.3],
        (1.5, 95): [0.0, 0.5, 1.0, 1.0, 1.1, 1.3, 1.5, 2.0, 2.4, 2.7, 3.1, 3.4, 3.9, 4.4, 5.0, 5.4, 5.8, 6.3, 6.7, 7.2,
                    7.7],
        (1.5, 90): [0.0, 0.5, 1.0, 1.3, 1.3, 1.5, 1.9, 2.2, 2.5, 2.9, 3.3, 3.8, 4.3, 4.7, 5.2, 5.6, 6.1, 6.5, 7.1, 7.6,
                    8.0],
        (1.5, 85): [0.0, 0.5, 1.0, 1.5, 1.5, 2.0, 2.2, 2.5, 3.0, 3.3, 3.7, 4.1, 4.4, 4.8, 5.3, 5.8, 6.2, 6.8, 7.2, 7.7,
                    8.1],
        (1.5, 80): [0.0, 0.5, 1.0, 1.5, 1.7, 2.1, 2.3, 2.7, 3.1, 3.4, 3.8, 4.1, 4.5, 4.9, 5.4, 5.9, 6.4, 6.9, 7.3, 7.8,
                    8.2],
        (1.5, 70): [0.0, 0.5, 1.0, 1.5, 2.0, 2.2, 2.5, 2.9, 3.2, 3.6, 3.9, 4.3, 4.7, 5.2, 5.6, 6.1, 6.6, 7.0, 7.5, 8.0,
                    8.4],
        (1.5, 60): [0.0, 0.5, 1.0, 1.5, 2.0, 2.3, 2.6, 3.0, 3.3, 3.7, 4.0, 4.4, 4.9, 5.4, 5.8, 6.3, 6.7, 7.2, 7.7, 8.2,
                    8.7],
        (1.5, 50): [0.0, 0.5, 1.0, 1.5, 2.0, 2.3, 2.6, 3.1, 3.4, 3.8, 4.2, 4.6, 5.2, 5.6, 6.0, 6.4, 6.9, 7.4, 8.0, 8.5,
                    9.0],
        (1.0, 95): [0.0, 0.5, 1.0, 0.8, 0.9, 1.0, 1.3, 1.7, 2.2, 2.6, 2.9, 3.3, 3.6, 4.0, 4.5, 5.0, 5.6, 6.1, 6.5, 6.9,
                    7.3],
        (1.0, 90): [0.0, 0.5, 1.0, 1.1, 1.1, 1.3, 1.5, 2.0, 2.4, 2.7, 3.1, 3.5, 4.0, 4.4, 5.0, 5.4, 5.9, 6.3, 6.7, 7.3,
                    7.8],
        (1.0, 85): [0.0, 0.5, 1.0, 1.3, 1.2, 1.4, 1.8, 2.1, 2.5, 2.9, 3.3, 3.7, 4.2, 4.7, 5.1, 5.6, 6.0, 6.5, 7.0, 7.5,
                    8.0],
        (1.0, 80): [0.0, 0.5, 1.0, 1.4, 1.3, 1.7, 1.9, 2.3, 2.7, 3.1, 3.5, 3.9, 4.4, 4.8, 5.2, 5.7, 6.2, 6.7, 7.2, 7.6,
                    8.1],
        (1.0, 70): [0.0, 0.5, 1.0, 1.5, 1.7, 2.0, 2.2, 2.6, 3.0, 3.4, 3.8, 4.1, 4.5, 4.9, 5.4, 5.9, 6.4, 6.8, 7.3, 7.8,
                    8.3],
        (1.0, 60): [0.0, 0.5, 1.0, 1.5, 1.9, 2.1, 2.4, 2.8, 3.1, 3.5, 3.9, 4.2, 4.6, 5.1, 5.6, 6.1, 6.5, 7.0, 7.5, 7.9,
                    8.4],
        (1.0, 50): [0.0, 0.5, 1.0, 1.5, 2.0, 2.2, 2.5, 2.9, 3.2, 3.6, 4.0, 4.4, 4.8, 5.3, 5.8, 6.2, 6.6, 7.2, 7.7, 8.2,
                    8.7],
        (0.8, 95): [0.0, 0.5, 1.0, 0.6, 0.8, 0.9, 1.2, 1.6, 2.1, 2.5, 2.9, 3.2, 3.6, 3.9, 4.3, 4.8, 5.3, 5.7, 6.4, 6.8,
                    7.2],
        (0.8, 90): [0.0, 0.5, 1.0, 0.9, 1.0, 1.2, 1.4, 1.9, 2.3, 2.7, 3.0, 3.4, 3.8, 4.2, 4.7, 5.3, 5.8, 6.2, 6.6, 7.1,
                    7.6],
        (0.8, 85): [0.0, 0.5, 1.0, 1.1, 1.1, 1.3, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0, 4.5, 5.0, 5.5, 5.9, 6.4, 6.8, 7.3,
                    7.8],
        (0.8, 80): [0.0, 0.5, 1.0, 1.3, 1.2, 1.4, 1.8, 2.1, 2.5, 2.9, 3.3, 3.8, 4.2, 4.7, 5.1, 5.6, 6.1, 6.5, 7.0, 7.5,
                    8.0],
        (0.8, 70): [0.0, 0.5, 1.0, 1.5, 1.5, 1.8, 2.1, 2.4, 2.8, 3.2, 3.6, 4.0, 4.4, 4.8, 5.3, 5.8, 6.3, 6.7, 7.2, 7.7,
                    8.2],
        (0.8, 60): [0.0, 0.5, 1.0, 1.5, 1.8, 2.0, 2.2, 2.6, 3.0, 3.4, 3.8, 4.2, 4.5, 5.0, 5.5, 6.0, 6.4, 6.9, 7.4, 7.8,
                    8.3],
        (0.8, 50): [0.0, 0.5, 1.0, 1.5, 1.9, 2.1, 2.4, 2.8, 3.1, 3.5, 3.9, 4.3, 4.7, 5.2, 5.7, 6.1, 6.5, 7.0, 7.5, 8.0,
                    8.5],
        (0.6, 95): [0.0, 0.5, 1.0, 0.5, 0.6, 0.8, 1.0, 1.2, 1.9, 2.4, 2.8, 3.1, 3.5, 3.8, 4.2, 4.5, 5.0, 5.5, 6.0, 6.7,
                    7.1],
        (0.6, 90): [0.0, 0.5, 1.0, 0.7, 0.9, 1.0, 1.3, 1.7, 2.1, 2.6, 2.9, 3.3, 3.6, 4.0, 4.5, 4.9, 5.4, 5.9, 6.5, 6.9,
                    7.4],
        (0.6, 85): [0.0, 0.5, 1.0, 0.9, 1.0, 1.1, 1.4, 1.8, 2.2, 2.7, 3.0, 3.4, 3.8, 4.3, 4.7, 5.2, 5.8, 6.2, 6.6, 7.1,
                    7.6],
        (0.6, 80): [0.0, 0.5, 1.0, 1.1, 1.1, 1.3, 1.6, 2.0, 2.4, 2.8, 3.1, 3.6, 4.0, 4.4, 4.9, 5.4, 5.9, 6.3, 6.8, 7.3,
                    7.8],
        (0.6, 70): [0.0, 0.5, 1.0, 1.4, 1.3, 1.5, 1.8, 2.2, 2.6, 3.0, 3.4, 3.8, 4.3, 4.7, 5.2, 5.7, 6.1, 6.6, 7.1, 7.5,
                    8.0],
        (0.6, 60): [0.0, 0.5, 1.0, 1.5, 1.5, 1.7, 2.1, 2.4, 2.8, 3.2, 3.6, 4.0, 4.4, 4.8, 5.3, 5.8, 6.3, 6.7, 7.2, 7.7,
                    8.2],
        (0.6, 50): [0.0, 0.5, 1.0, 1.5, 1.7, 1.9, 2.2, 2.6, 3.0, 3.4, 3.8, 4.1, 4.5, 5.0, 5.5, 6.0, 6.4, 6.9, 7.4, 7.9,
                    8.4],
        (0.4, 95): [0.0, 0.5, 0.9, 0.5, 0.5, 0.6, 0.7, 0.9, 1.0, 1.8, 2.2, 2.6, 3.1, 3.7, 4.1, 4.4, 4.7, 5.1, 5.6, 6.1,
                    6.5],
        (0.4, 90): [0.0, 0.5, 1.0, 0.5, 0.6, 0.8, 1.1, 1.2, 1.9, 2.4, 2.8, 3.1, 3.5, 3.9, 4.2, 4.6, 5.1, 5.6, 6.0, 6.7,
                    7.1],
        (0.4, 85): [0.0, 0.5, 1.0, 0.6, 0.8, 0.9, 1.2, 1.6, 2.1, 2.5, 2.9, 3.3, 3.7, 4.0, 4.4, 4.9, 5.3, 5.9, 6.4, 6.9,
                    7.3],
        (0.4, 80): [0.0, 0.5, 1.0, 0.8, 0.9, 1.0, 1.4, 1.8, 2.2, 2.6, 3.0, 3.4, 3.8, 4.2, 4.7, 5.1, 5.6, 6.1, 6.6, 7.0,
                    7.5],
        (0.4, 70): [0.0, 0.5, 1.0, 1.1, 1.1, 1.3, 1.6, 1.9, 2.4, 2.8, 3.2, 3.6, 4.0, 4.4, 4.9, 5.4, 5.9, 6.4, 6.8, 7.3,
                    7.8],
        (0.4, 60): [0.0, 0.5, 1.0, 1.3, 1.4, 1.5, 1.8, 2.1, 2.5, 3.0, 3.4, 3.8, 4.2, 4.7, 5.1, 5.6, 6.1, 6.6, 7.0, 7.5,
                    8.0],
        (0.4, 50): [0.0, 0.5, 1.0, 1.5, 1.6, 1.7, 1.9, 2.3, 2.7, 3.2, 3.6, 4.0, 4.4, 4.8, 5.3, 5.8, 6.3, 6.7, 7.2, 7.7,
                    8.2],
        (0.2, 95): [0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.7, 2.6, 2.7, 3.0, 3.4, 3.9, 4.3, 4.7, 5.1, 5.5, 5.6,
                    5.9],
        (0.2, 90): [0.0, 0.5, 0.8, 0.5, 0.5, 0.5, 0.6, 0.6, 0.7, 0.9, 2.6, 3.1, 3.4, 3.5, 4.0, 4.3, 4.7, 5.1, 5.5, 5.9,
                    6.4],
        (0.2, 85): [0.0, 0.5, 1.0, 0.5, 0.5, 0.6, 0.8, 0.8, 1.0, 1.3, 3.0, 3.4, 3.7, 3.8, 4.1, 4.5, 4.8, 5.3, 5.7, 6.2,
                    6.7],
        (0.2, 80): [0.0, 0.5, 1.0, 0.5, 0.5, 0.7, 1.0, 1.1, 1.2, 1.9, 3.1, 3.5, 3.8, 4.0, 4.2, 4.6, 5.0, 5.5, 6.0, 6.5,
                    7.1],
        (0.2, 70): [0.0, 0.5, 1.0, 0.6, 0.7, 0.9, 1.2, 1.5, 2.0, 2.5, 3.3, 3.6, 4.0, 4.4, 4.9, 5.3, 5.8, 6.1, 6.6, 6.9,
                    7.3],
        (0.2, 60): [0.0, 0.5, 1.0, 0.8, 0.9, 1.0, 1.4, 1.7, 2.2, 2.6, 3.4, 3.8, 4.2, 4.7, 5.1, 5.6, 6.1, 6.6, 7.1, 7.6,
                    7.8],
        (0.2, 50): [0.0, 0.5, 1.0, 1.1, 1.0, 1.2, 1.6, 1.9, 2.4, 2.8, 3.6, 4.0, 4.4, 4.8, 5.3, 5.9, 6.4, 6.9, 7.3, 7.8,
                    7.8],
        (0.1, 95): [0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 2.6, 3.0, 3.2, 3.3, 3.9, 4.3, 4.7, 4.9, 5.3,
                    5.6],
        (0.1, 90): [0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 2.7, 3.0, 3.2, 3.7, 4.1, 4.5, 4.9, 5.2, 5.6,
                    5.9],
        (0.1, 85): [0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 2.7, 3.1, 3.3, 3.8, 4.2, 4.6, 5.0, 5.3, 5.7,
                    6.2],
        (0.1, 80): [0.0, 0.5, 0.8, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.6, 2.7, 3.2, 3.4, 3.9, 4.3, 4.7, 5.1, 5.4, 5.9,
                    6.4],
        (0.1, 70): [0.0, 0.5, 0.9, 0.5, 0.5, 0.6, 0.7, 0.6, 0.8, 1.0, 2.4, 2.7, 3.3, 3.4, 3.9, 4.5, 4.9, 5.3, 5.8, 6.3,
                    6.8],
        (0.1, 60): [0.0, 0.5, 1.0, 0.5, 0.5, 0.7, 1.0, 1.1, 1.2, 2.2, 2.5, 2.7, 3.5, 3.7, 4.3, 4.7, 5.1, 5.6, 6.1, 6.6,
                    7.1],
        (0.1, 50): [0.0, 0.5, 1.0, 0.5, 0.7, 0.9, 1.2, 1.5, 1.4, 2.4, 2.8, 3.3, 3.7, 4.5, 4.9, 5.3, 5.8, 6.4, 6.9, 6.9,
                    7.4]
    }
}

# 提取所有TRD和CDF值
TRD_VALS = sorted(set(trd for trd, _ in DESIGN_DATA['columns'].keys()))
CDF_VALS = sorted(set(cdf for _, cdf in DESIGN_DATA['columns'].keys()))


# ---- 修改后的插值函数 ----
def interpolate_y(x_target, trd_target, cdf_target):
    if x_target not in DESIGN_DATA['x_values']:
        raise ValueError(f"x={x_target} not in data.")

    # 获取x_target在x_values中的索引
    idx = DESIGN_DATA['x_values'].index(x_target)

    # 如果存在精确匹配，直接返回
    if (trd_target, cdf_target) in DESIGN_DATA['columns']:
        return DESIGN_DATA['columns'][(trd_target, cdf_target)][idx]

    # 检查TRD和CDF是否在范围内
    if not (TRD_VALS[0] <= trd_target <= TRD_VALS[-1]):
        raise ValueError("TRD out of range.")
    if not (CDF_VALS[0] <= cdf_target <= CDF_VALS[-1]):
        raise ValueError("CDF out of range.")

    # 找到TRD和CDF的四个周围点
    i_t = bisect.bisect_left(TRD_VALS, trd_target)
    low_t = TRD_VALS[max(i_t - 1, 0)]
    high_t = TRD_VALS[min(i_t, len(TRD_VALS) - 1)]

    i_c = bisect.bisect_left(CDF_VALS, cdf_target)
    low_c = CDF_VALS[max(i_c - 1, 0)]
    high_c = CDF_VALS[min(i_c, len(CDF_VALS) - 1)]

    # 获取四个角点的y值
    def get_y(trd, cdf):
        if (trd, cdf) in DESIGN_DATA['columns']:
            return DESIGN_DATA['columns'][(trd, cdf)][idx]
        return np.nan

    y11 = get_y(low_t, low_c)
    y12 = get_y(low_t, high_c)
    y21 = get_y(high_t, low_c)
    y22 = get_y(high_t, high_c)

    # 如果任意一个值为nan，则返回nan
    if np.isnan(y11) or np.isnan(y12) or np.isnan(y21) or np.isnan(y22):
        return np.nan

    # 如果四个点重合，则返回该值
    if low_t == high_t and low_c == high_c:
        return y11
    if low_t == high_t:
        return y11 + (y12 - y11) * (cdf_target - low_c) / (high_c - low_c)
    if low_c == high_c:
        return y11 + (y21 - y11) * (trd_target - low_t) / (high_t - low_t)

    # 双线性插值
    return (y11 * (high_t - trd_target) * (high_c - cdf_target) +
            y21 * (trd_target - low_t) * (high_c - cdf_target) +
            y12 * (high_t - trd_target) * (cdf_target - low_c) +
            y22 * (trd_target - low_t) * (cdf_target - low_c)) / ((high_t - low_t) * (high_c - low_c))


# ---- GUI Application ----
class CurveGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Objective Design Curve Generator")
        self.data = None
        self.modified_data = None
        self.intervals = []  # Store interval configurations

        self.create_widgets()
        self.setup_layout()
        self.add_interval_row(start_Dpdf=0.0, end_Dpdf=10.0, trd=1.0, cdf=90)  # Add a default covering interval

    def create_widgets(self):
        # Top-left: Parameters
        self.param_frame = ttk.Frame(self.root, padding=10)
        self.param_frame.grid(row=0, column=0, sticky='nw')

        # Interval Configuration
        ttk.Label(self.param_frame, text="Displacement Intervals:").grid(row=0, column=0, columnspan=5, pady=5)
        self.interval_container = ttk.Frame(self.param_frame)
        self.interval_container.grid(row=1, column=0, columnspan=5, sticky='ew')

        # Interval headers
        headers = ['Start Dpdf', 'End Dpdf', 'TRD', 'Peg (%)']
        for col, text in enumerate(headers):
            ttk.Label(self.interval_container, text=text).grid(row=0, column=col, padx=2)

        # Add/Remove buttons
        btn_frame = ttk.Frame(self.param_frame)
        btn_frame.grid(row=2, column=0, columnspan=5, pady=5)
        ttk.Button(btn_frame, text="+ Add Interval", command=self.add_interval_row).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="- Remove Last", command=self.remove_interval_row).pack(side=tk.LEFT, padx=2)

        # Structural Parameters
        ttk.Label(self.param_frame, text="Yield Strain of longitudinal reinforcement (Unit: 1):").grid(row=3, column=0, sticky='w', pady=2)
        self.entry_A = ttk.Entry(self.param_frame, width=10)
        self.entry_A.grid(row=3, column=1, padx=5, pady=2)
        self.entry_A.insert(0, "0.002")

        ttk.Label(self.param_frame, text="Column Height (Unit: m):").grid(row=4, column=0, sticky='w', pady=2)
        self.entry_B = ttk.Entry(self.param_frame, width=10)
        self.entry_B.grid(row=4, column=1, padx=5, pady=2)
        self.entry_B.insert(0, "5.0")

        ttk.Label(self.param_frame, text="Diameter (Unit: m):").grid(row=5, column=0, sticky='w', pady=2)
        self.entry_D = ttk.Entry(self.param_frame, width=10)
        self.entry_D.grid(row=5, column=1, padx=5, pady=2)
        self.entry_D.insert(0, "1.0")

        ttk.Button(self.param_frame, text="Generate Curves", command=self.show_target_curve).grid(row=9, columnspan=5,
                                                                                                  pady=10)

        # Adding Labels for Dpdf, Dsdf, Dpd, Dsd right next to "Yield Strain"
        ttk.Label(self.param_frame, text="Dpdf: Peak displacement ductility factor, 0.0≤Dpdf≤10.0",
                  font=("Arial", 10, "bold")).grid(row=3, column=2, padx=10, pady=5)
        ttk.Label(self.param_frame, text="Dsdf: Static residual displacement ductility factor, 0.0≤Dsdf≤10.0",
                  font=("Arial", 10, "bold")).grid(row=4, column=2, padx=10, pady=5)
        ttk.Label(self.param_frame, text="Dpd: Peak displacement (m)", font=("Arial", 10, "bold")).grid(row=5, column=2,
                                                                                                        padx=10, pady=5)
        ttk.Label(self.param_frame, text="Dsd: Static residual displacement (m); ", font=("Arial", 10, "bold")).grid(
            row=6, column=2, padx=10, pady=5)
        ttk.Label(self.param_frame, text="TRD:Target residual displacement ductility factor, 0.1≤TRD≤2.0",
                  font=("Arial", 10, "bold")).grid(row=7, column=2, padx=10, pady=5)
        ttk.Label(self.param_frame, text="Peg:Expected guarantee, 50%≤Peg≤95%", font=("Arial", 10, "bold")).grid(row=8,
                                                                                                                 column=2,
                                                                                                                 padx=10,
                                                                                                                 pady=5)

        # Bottom-left: Data Tables
        self.table_frame = ttk.Frame(self.root, padding=10)
        self.table_frame.grid(row=1, column=0, sticky='nsew')

        # Table Header
        header_frame = ttk.Frame(self.table_frame)
        header_frame.pack(fill='x', pady=5)
        ttk.Label(header_frame, text="Design target (Ductility)").pack(side=tk.LEFT, padx=40)
        ttk.Label(header_frame, text="Design target (Displacement)").pack(side=tk.RIGHT, padx=40)

        # Table Content
        content_frame = ttk.Frame(self.table_frame)
        content_frame.pack(fill='both', expand=True)

        self.orig_tree = ttk.Treeview(content_frame, columns=("X", "Y"), show="headings", height=12)
        self.orig_tree.heading("X", text="Dpdf")
        self.orig_tree.heading("Y", text="Dsdf")
        self.orig_tree.pack(side=tk.LEFT, fill='both', expand=True, padx=5)

        self.mod_tree = ttk.Treeview(content_frame, columns=("X", "Y"), show="headings", height=12)
        self.mod_tree.heading("X", text="Dpd (m)")
        self.mod_tree.heading("Y", text="Dsd (m)")
        self.mod_tree.pack(side=tk.RIGHT, fill='both', expand=True, padx=5)

        # Right-side: Plots
        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.grid(row=0, column=1, rowspan=2, sticky='nsew')

        # Original Plot
        self.orig_fig, self.orig_ax = plt.subplots(figsize=(6, 4))
        self.orig_canvas = FigureCanvasTkAgg(self.orig_fig, master=self.plot_frame)
        self.orig_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Modified Plot
        self.mod_fig, self.mod_ax = plt.subplots(figsize=(6, 4))
        self.mod_canvas = FigureCanvasTkAgg(self.mod_fig, master=self.plot_frame)
        self.mod_canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Export Button
        ttk.Button(self.root, text="Export Data", command=self.export_data).grid(row=2, columnspan=2, pady=10)

    def add_interval_row(self, start_Dpdf=0.0, end_Dpdf=10.0, trd=1.0, cdf=90):
        row_idx = len(self.intervals) + 1  # Start from row 1 (0 is header)
        entries = []
        for col in range(4):
            e = ttk.Entry(self.interval_container, width=8)
            e.grid(row=row_idx, column=col, padx=2, pady=2)
            entries.append(e)
        entries[0].insert(0, str(start_Dpdf))
        entries[1].insert(0, str(end_Dpdf))
        entries[2].insert(0, str(trd))
        entries[3].insert(0, str(cdf))
        self.intervals.append(entries)

    def remove_interval_row(self):
        if len(self.intervals) > 0:
            for entry in self.intervals[-1]:
                entry.destroy()
            self.intervals.pop()

    def get_interval_configs(self):
        configs = []
        for entries in self.intervals:
            try:
                start_Dpdf = float(entries[0].get())
                end_Dpdf = float(entries[1].get())
                trd = float(entries[2].get())
                cdf = float(entries[3].get())
                configs.append((start_Dpdf, end_Dpdf, trd, cdf))
            except ValueError:
                continue
        # Sort by start_x
        configs.sort(key=lambda x: x[0])
        return configs

    def setup_layout(self):
        self.root.geometry("1280x720")
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

    def calculate_Uy(self):
        try:
            A = float(self.entry_A.get())
            B = float(self.entry_B.get())
            D = float(self.entry_D.get())
            return 1.125 * A * B ** 2 / (3 * D)
        except ValueError:
            messagebox.showerror("Error", "Invalid parameter values")
            return None

    def show_target_curve(self):
        configs = self.get_interval_configs()
        if not configs:
            messagebox.showerror("Error", "No valid interval configurations")
            return

        Uy = self.calculate_Uy()
        if Uy is None:
            return

        x_vals = np.arange(0, 10.01, 0.5)
        y_vals = []
        for x in x_vals:
            trd, cdf = None, None
            for start, end, t, c in configs:
                if start <= x <= end:
                    trd, cdf = t, c
                    # Highlight the background for the current interval range
                    self.orig_ax.axvspan(start, end, color='lightgray', alpha=0.5)  # Add background color to the range
                    break
            if trd is None:
                y_vals.append(np.nan)
                continue

            try:
                y = interpolate_y(x, trd, cdf)
            except ValueError as e:
                print(f"Interpolation error for x={x}, TRD={trd}, CDF={cdf}: {e}")
                y = np.nan
            y_vals.append(y)

        self.data = pd.DataFrame({'X': x_vals, 'Y': y_vals})
        self.modified_data = pd.DataFrame({
            'X': self.data['X'] * Uy,
            'Y': self.data['Y'] * Uy
        })

        self.update_tables()
        self.plot_curves(configs)
        self.update_plot_titles(configs, Uy)

    def update_plot_titles(self, configs, Uy):
        title_parts = []
        for start, end, trd, cdf in configs:
            title_parts.append(f"{start}-{end}: TRD={trd}, Peg={cdf}%")
        self.orig_ax.set_title("Design target (Ductility)\n" + "\n".join(title_parts), fontsize=8)
        self.mod_ax.set_title(f"Design target (Displacement) (Uy={Uy:.4f})", fontsize=10)
        self.orig_canvas.draw_idle()
        self.mod_canvas.draw_idle()

    def update_tables(self):
        # Clear tables first
        for tree in [self.orig_tree, self.mod_tree]:
            for row in tree.get_children():
                tree.delete(row)

        # Fill original data table
        if self.data is not None:
            for _, row in self.data.iterrows():
                self.orig_tree.insert("", "end",
                                      values=(f"{row['X']:.2f}", f"{row['Y']:.2f}" if pd.notna(row['Y']) else ""))

        # Fill modified data table
        if self.modified_data is not None:
            for _, row in self.modified_data.iterrows():
                self.mod_tree.insert("", "end",
                                     values=(f"{row['X']:.4f}", f"{row['Y']:.4f}" if pd.notna(row['Y']) else ""))

    def plot_curves(self, configs):
        # Clear previous plots
        self.orig_ax.clear()
        self.mod_ax.clear()

        # Define background colors to cycle through
        bg_colors = ['lightgray', 'lightcoral', 'lightskyblue', 'lightgreen', 'lightsalmon']

        # Plot original data with background highlighting
        if self.data is not None:
            self.orig_ax.plot(self.data['X'].to_numpy(), self.data['Y'].to_numpy(), marker='o', linestyle='-',
                              color='tab:blue')
            self.orig_ax.set_xlabel("Dpdf")
            self.orig_ax.set_ylabel("Dsdf")
            self.orig_ax.grid(True)
            for i, (start, end, _, _) in enumerate(configs):
                color_index = i % len(bg_colors)
                self.orig_ax.axvspan(start, end, facecolor=bg_colors[color_index], alpha=0.2)

        # Plot modified data with background highlighting
        if self.modified_data is not None:
            self.mod_ax.plot(self.modified_data['X'].to_numpy(), self.modified_data['Y'].to_numpy(), marker='o',
                             linestyle='-',
                             color='tab:orange')
            self.mod_ax.set_xlabel("Dpd (m)")
            self.mod_ax.set_ylabel("Dsd (m)")
            self.mod_ax.grid(True)
            for i, (start, end, _, _) in enumerate(configs):
                color_index = i % len(bg_colors)
                start_dpd = start * self.calculate_Uy()
                end_dpd = end * self.calculate_Uy()
                self.mod_ax.axvspan(start_dpd, end_dpd, facecolor=bg_colors[color_index], alpha=0.2)

        # Redraw the canvases
        self.orig_canvas.draw()
        self.mod_canvas.draw()

    def export_data(self):
        if self.data is None or self.modified_data is None or not self.intervals:
            messagebox.showwarning("Warning", "No data or intervals to export")
            return

        exported_rows = []
        uy = self.calculate_Uy()
        if uy is None:
            return

        x_vals = self.data['X'].to_numpy()
        y_vals = self.data['Y'].to_numpy()
        dpd_vals = self.modified_data['X'].to_numpy()
        dsd_vals = self.modified_data['Y'].to_numpy()

        configs = self.get_interval_configs()

        for i in range(len(x_vals)):
            dpdf = x_vals[i]
            trd = None
            peg = None
            for start, end, t, p in configs:
                if start <= dpdf <= end:
                    trd = t
                    peg = p
                    break
                elif i > 0 and start <= x_vals[i - 1] <= end and (dpdf < start):
                    # Handle the case where the current Dpdf is just outside the previous interval
                    trd = t
                    peg = p
                    break
                elif i < len(x_vals) - 1 and start <= x_vals[i + 1] <= end and (dpdf > end):
                    # Handle the case where the current Dpdf is just outside the next interval
                    trd = t
                    peg = p
                    break
            exported_rows.append({
                'TRD': trd,
                'Peg (%)': peg,
                'Dpdf': dpdf,
                'Dsdf': y_vals[i],
                'Dpd (m)': dpd_vals[i],
                'Dsd (m)': dsd_vals[i]
            })

        combined_df = pd.DataFrame(exported_rows)

        path = filedialog.asksaveasfilename(
            defaultextension='.xlsx',
            filetypes=[('Excel Files', '*.xlsx')]
        )
        if not path:
            return
        try:
            combined_df.to_excel(path, index=False)
            messagebox.showinfo("Success", f"Data has been exported to:\n{path}")
        except Exception as e:
            messagebox.showerror("Export data failed", str(e))


if __name__ == '__main__':
    root = tk.Tk()
    app = CurveGeneratorApp(root)
    root.mainloop()


# 后台调用接口
def get_design_objective_curve(epsilon_y, column_H, column_D, U_y_structure,
                               intervals=[(0.0, 10.0, 1.0, 90)]):
    """
    后台调用接口：根据屈服应变、墩高、直径，输出目标曲线（Dpd-Dsd对）
    参数单位要求：
        - epsilon_y: 屈服应变 (单位为 1，如0.002)
        - column_H: 墩柱高度 (m)
        - column_D: 墩柱直径 (m)
    返回：
        DataFrame，包含 'Dpd (m)' 和 'Dsd (m)' 两列
    """
    Uy = U_y_structure  # 1.125 * epsilon_y * column_H ** 2 / (3 * column_D)
    x_vals = np.arange(0, 10.01, 0.5)
    y_vals = []

    for x in x_vals:
        trd, cdf = None, None
        for start, end, t, c in intervals:
            if start <= x <= end:
                trd, cdf = t, c
                break
        if trd is None:
            y_vals.append(np.nan)
            continue
        try:
            y = interpolate_y(x, trd, cdf)
        except Exception as e:
            print(f"Interpolation error at x={x}: {e}")
            y = np.nan
        y_vals.append(y)

    Dpd = x_vals * Uy
    Dsd = np.array(y_vals) * Uy
    return pd.DataFrame({'Dpd (m)': Dpd, 'Dsd (m)': Dsd})