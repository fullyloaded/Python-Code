import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # 在 Windows 上使用 TkAgg 後端
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from scipy import signal
from matplotlib.patches import FancyArrowPatch
from PIL import Image
import os
import glob
import warnings

# 設定中文字型和數學符號字型
try:
    # 主要字型：Microsoft YaHei 用於中文
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Noto Sans CJK SC', 'DejaVu Sans']
    # 數學字型：STIX 用於數學符號（如 ℏ, ω）
    plt.rcParams['mathtext.fontset'] = 'stix'
    plt.rcParams['axes.unicode_minus'] = False  # 確保負號顯示正確
except Exception as e:
    print(f"警告：無法載入字型，圖表中的中文或數學符號可能無法正確顯示。錯誤：{e}")
    # 回退到預設字型
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    plt.rcParams['mathtext.fontset'] = 'dejavusans'

# 驗證字型是否支援 ℏ
def check_hbar_support():
    font_list = [f.name for f in fm.fontManager.ttflist]
    if 'STIXGeneral' in font_list:
        print("STIXGeneral 可用，將用於渲染 ℏ")
        return 'STIXGeneral'
    elif 'DejaVu Sans' in font_list:
        print("DejaVu Sans 可用，將用於渲染 ℏ")
        return 'DejaVu Sans'
    else:
        print("警告：未找到 STIXGeneral 或 DejaVu Sans，將使用 LaTeX 渲染並回退到預設字型")
        return 'DejaVu Sans'  # 預設回退字型，防止 fontfamily=None

# 列印可用字型以供除錯
def print_available_fonts():
    font_list = sorted(set(f.name for f in fm.fontManager.ttflist))
    print("可用字型：", font_list)

# 通用參數
時間 = np.linspace(0, 4 * np.pi, 1000)  # Plot 1 和 Plot 3 的時間陣列
方波時間 = np.linspace(0, 4, 1000)     # Plot 2 的時間陣列
ω = 1                                  # 角頻率 (Unicode: U+03C9)
電容 = 1                               # 電容值
ℏ = 1.0545718e-34                      # 約化普朗克常數 (Unicode: U+210F)

# Plot 1: 電壓與電流波形
def 繪製電壓電流():
    電壓 = np.cos(ω * 時間)
    電流 = 電容 * ω * np.sin(ω * 時間)
    
    圖表, 軸 = plt.subplots(figsize=(8, 5))
    軸.plot(時間, 電壓, 'b-', label='電壓 V(t) = cos(ωt)')
    軸.plot(時間, 電流, 'r--', label='電流 I(t) = Cω sin(ωt)')
    軸.axvline(np.pi/4, color='k', linestyle=':', label='t = π/4')  # π: U+03C0
    軸.annotate('電流最大，電壓上升', xy=(np.pi/4, 1), xytext=(np.pi/2, 1.3),
                arrowprops=dict(facecolor='black', shrink=0.05))
    
    # 插圖：儲水池類比
    插圖軸 = 軸.inset_axes([0.6, 0.1, 0.3, 0.3])
    插圖時間 = np.linspace(0, 2 * np.pi, 100)
    插圖軸.plot(插圖時間, np.cos(插圖時間), 'b-', label='水位')
    插圖軸.arrow(np.pi/4, 0, 0, 1, head_width=0.1, head_length=0.2, fc='r', ec='r', label='流量')
    插圖軸.set_title('儲水池類比', fontsize=8)
    插圖軸.set_xticks([]); 插圖軸.set_yticks([])
    插圖軸.text(0.1, 1.0, '流量領先 π/2', fontsize=8)
    
    軸.set_xlabel('時間 (秒)')
    軸.set_ylabel('振幅')
    軸.set_title('電容器中的電壓與電流 (ω = 1, C = 1)')
    軸.grid(True)
    軸.legend()
    plt.tight_layout()
    plt.savefig('voltage_current.png', dpi=300)
    plt.close()

# Plot 2: 方波的傅立葉變換
def 繪製方波傅立葉():
    方波 = signal.square(2 * np.pi * 方波時間)
    傅立葉 = np.fft.fft(方波)
    頻率 = np.fft.fftfreq(len(方波時間), 方波時間[1] - 方波時間[0])
    正頻率 = 頻率 > 0
    頻率 = 頻率[正頻率]
    傅立葉幅度 = np.abs(傅立葉)[正頻率]
    
    圖表, (軸1, 軸2) = plt.subplots(2, 1, figsize=(8, 6))
    軸1.plot(方波時間, 方波, 'b-', label='方波')
    軸1.set_xlabel('時間 (秒)')
    軸1.set_ylabel('振幅')
    軸1.set_title('時域方波')
    軸1.grid(True)
    軸1.legend()
    
    軸2.stem(頻率, 傅立葉幅度, 'b', label='幅度譜')
    軸2.set_xlabel('頻率 (Hz)')
    軸2.set_ylabel('幅度')
    軸2.set_title('頻域譜 (奇次諧波)')
    軸2.grid(True)
    軸2.legend()
    軸2.text(0.5, max(傅立葉幅度) * 0.9, '與量子能級相關 (Plot 4)', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('square_wave_fft.png', dpi=300)
    plt.close()

# Plot 3: 歐拉公式與量子相位動畫
def 繪製單位圓動畫():
    圖表, 軸 = plt.subplots(figsize=(8, 8))
    θ = np.linspace(0, 2 * np.pi, 100)  # θ: U+03B8
    軸.plot(np.cos(θ), np.sin(θ), 'k-', label='單位圓')
    軸.axhline(0, color='k', alpha=0.3); 軸.axvline(0, color='k', alpha=0.3)
    
    # 初始向量
    初始時間 = np.pi / 4
    電壓向量, = 軸.plot([0, np.cos(ω * 初始時間)], [0, np.sin(ω * 初始時間)], 'b-', lw=2, label='電壓 (cos(ωt))')
    電流向量, = 軸.plot([0, np.sin(ω * 初始時間)], [0, np.cos(ω * 初始時間)], 'r--', lw=2, label='電流 (sin(ωt))')
    量子向量, = 軸.plot([0, 0.5 * np.cos(ω * 初始時間 + np.pi/4)], [0, 0.5 * np.sin(ω * 初始時間 + np.pi/4)],
                         'c-', lw=2, label='量子 (45° 起始)')
    
    # 插圖：儲水池類比
    插圖軸 = 軸.inset_axes([0.1, 0.1, 0.3, 0.3])
    插圖時間 = np.linspace(0, 2 * np.pi, 100)
    插圖軸.plot(插圖時間, np.cos(插圖時間), 'b-', label='水位')
    插圖軸.arrow(np.pi/4, 0, 0, 1, head_width=0.1, head_length=0.2, fc='r', ec='r', label='流量')
    插圖軸.set_title('儲水池類比', fontsize=8)
    插圖軸.set_xticks([]); 插圖軸.set_yticks([])
    插圖軸.text(0.1, 1.0, '流量領先 π/2', fontsize=8)
    
    軸.set_xlabel('實部')
    軸.set_ylabel('虛部')
    軸.set_title('歐拉公式: e^jθ = cos(θ) + j sin(θ)')
    軸.set_xlim(-1.5, 1.5); 軸.set_ylim(-1.5, 1.5)
    軸.grid(True)
    軸.legend()
    軸.text(0.1, 1.3, '電流比電壓領先 90°。\n量子相位從 45° 開始並演化。', fontsize=10)
    
    def 更新(幀):
        時間值 = 幀
        電壓向量.set_data([0, np.cos(ω * 時間值)], [0, np.sin(ω * 時間值)])
        電流向量.set_data([0, np.sin(ω * 時間值)], [0, np.cos(ω * 時間值)])
        量子向量.set_data([0, 0.5 * np.cos(ω * 時間值 + np.pi/4)],
                           [0, 0.5 * np.sin(ω * 時間值 + np.pi/4)])
        return 電壓向量, 電流向量, 量子向量
    
    最終GIF = 'euler_animation.gif'
    臨時幀目錄 = 'temp_frames'
    os.makedirs(臨時幀目錄, exist_ok=True)
    
    try:
        # 生成幀
        幀列表 = np.arange(0, 2 * np.pi, 0.1)
        if len(幀列表) == 0:
            raise ValueError("未生成任何幀；請檢查幀範圍")
        
        print(f"正在為動畫生成 {len(幀列表)} 幀")
        for i, 幀 in enumerate(幀列表):
            更新(幀)
            圖表.canvas.draw()
            plt.savefig(os.path.join(臨時幀目錄, f'frame_{i:04d}.png'), dpi=300)
        
        # 使用 Pillow 將幀合併為 GIF
        幀檔案 = sorted(glob.glob(os.path.join(臨時幀目錄, 'frame_*.png')))
        if not 幀檔案:
            raise ValueError("在 temp_frames 目錄中未找到幀檔案")
        
        print(f"正在將 {len(幀檔案)} 幀合併為 GIF")
        圖像列表 = [Image.open(幀檔案路徑) for 幀檔案路徑 in 幀檔案]
        if not 圖像列表:
            raise ValueError("未從幀檔案載入任何圖像")
        
        圖像列表[0].save(
            最終GIF,
            save_all=True,
            append_images=圖像列表[1:],
            duration=50,  # 每幀 50 毫秒 (20 fps)
            loop=0  # 無限循環
        )
        
        # 清理臨時幀
        for 幀檔案路徑 in 幀檔案:
            os.remove(幀檔案路徑)
        os.rmdir(臨時幀目錄)
        
    except Exception as e:
        print(f"動畫生成過程中發生錯誤: {e}")
    finally:
        plt.close()

# Plot 4: 普朗克-愛因斯坦關係
def 繪製普朗克愛因斯坦():
    print_available_fonts()  # 除錯：列印可用字型
    頻率 = np.linspace(0, 1e15, 1000)  # 頻率 (Hz)
    能量 = ℏ * 2 * np.pi * 頻率      # E = ℏω (ω = 2πf)
    波長 = 3e8 / 頻率[1:]             # c / f (避免除以零)
    
    圖表, 軸1 = plt.subplots(figsize=(8, 5))
    # 檢查字型並選擇適當的標籤方式
    math_font = check_hbar_support()
    # 優先使用 LaTeX 渲染以確保 ℏ 正確顯示
    軸1.plot(頻率, 能量, 'b-', label=r'E = \hbar \omega')
    
    軸1.set_xlabel('頻率 (Hz)')
    軸1.set_ylabel('能量 (J)', color='b')
    軸1.tick_params(axis='y', labelcolor='b')
    軸1.set_title('普朗克-愛因斯坦關係')
    軸1.grid(True)
    
    # 輔助軸：波長
    軸2 = 軸1.twinx()
    軸2.plot(頻率[1:], 波長, 'g--', label='波長')
    軸2.set_ylabel('波長 (m)', color='g')
    軸2.tick_params(axis='y', labelcolor='g')
    
    # 註解
    軸1.text(0.5e15, max(能量) * 0.9, '量子儲水池：\n能量 (水位) ∝ 頻率 (流量)', fontsize=10)  # ∝: U+221D
    軸1.text(0.5e15, max(能量) * 0.7, '經典：連續\n量子：離散能級', fontsize=10)
    
    軸1.legend(loc='upper left')
    軸2.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig('planck_einstein.png', dpi=300)
    plt.close()

# 主函數：生成所有圖表
def 主程式():
    繪製電壓電流()
    繪製方波傅立葉()
    繪製單位圓動畫()
    繪製普朗克愛因斯坦()
    print("所有圖表生成成功：voltage_current.png, square_wave_fft.png, euler_animation.gif, planck_einstein.png")

if __name__ == "__main__":
    主程式()