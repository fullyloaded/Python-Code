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

# 設定中文字型
from matplotlib.font_manager import FontProperties
try:
    font_path = 'C:/Windows/Fonts/msyh.ttc'  # Windows 上的 Microsoft YaHei
    font = FontProperties(fname=font_path, size=10)
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Noto Sans CJK SC', 'DejaVu Sans']
    plt.rcParams['mathtext.fontset'] = 'stix'  # 使用 STIX 渲染數學符號
    plt.rcParams['axes.unicode_minus'] = False  # 確保負號顯示正確
except Exception as e:
    print(f"警告：無法載入字型，圖表中的中文或數學符號可能無法正確顯示。錯誤：{e}")
    font = FontProperties(family='DejaVu Sans', size=10)
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    plt.rcParams['mathtext.fontset'] = 'dejavusans'

# 通用參數
時間 = np.linspace(0, 4 * np.pi, 1000)  # 圖 1 和圖 3 的時間陣列
方波時間 = np.linspace(0, 4, 1000)     # 圖 2 的時間陣列
ω = 1                                  # 角頻率 (rad/s, U+03C9)
電容 = 1                               # 電容 (F)
電感 = 1                               # 電感 (H)
ℏ = 1.0545718e-34                      # 約化普朗克常數 (J·s, U+210F)

# 圖 1: 電容器 V(t)、I(t) 時域 vs 頻域波形
def 繪製電壓電流():
    電壓 = np.cos(ω * 時間)
    電流 = 電容 * ω * np.sin(ω * 時間)
    
    圖表, (軸1, 軸2) = plt.subplots(2, 1, figsize=(8, 6))
    # 時域
    軸1.plot(時間, 電壓, 'b-', label=r'電壓 $V(t) = \cos(\omega t)$')
    軸1.plot(時間, 電流, 'r--', label=r'電流 $I(t) = C \omega \sin(\omega t)$')
    軸1.axvline(np.pi/4, color='k', linestyle=':', label=r'$t = \pi/4$')
    軸1.annotate('電流最大，電壓上升', xy=(np.pi/4, 1), xytext=(np.pi/2, 1.3),
                 arrowprops=dict(facecolor='black', shrink=0.05), fontproperties=font)
    軸1.set_xlabel('時間 (秒)', fontproperties=font)
    軸1.set_ylabel('振幅', fontproperties=font)
    軸1.set_title('電容器時域波形', fontproperties=font)
    軸1.grid(True)
    軸1.legend()
    
    # 插圖：儲水池類比
    插圖軸 = 軸1.inset_axes([0.6, 0.1, 0.3, 0.3])
    插圖時間 = np.linspace(0, 2 * np.pi, 100)
    插圖軸.plot(插圖時間, np.cos(插圖時間), 'b-', label='水位')
    插圖軸.arrow(np.pi/4, 0, 0, 1, head_width=0.1, head_length=0.2, fc='r', ec='r', label='流量')
    插圖軸.set_title('儲水池類比', fontsize=8, fontproperties=font)
    插圖軸.set_xticks([]); 插圖軸.set_yticks([])
    插圖軸.text(0.1, 1.0, r'流量領先 $\pi/2$', fontsize=8, fontproperties=font)
    
    # 頻域
    電壓傅立葉 = np.abs(np.fft.fft(電壓))[0:len(電壓)//2]
    電流傅立葉 = np.abs(np.fft.fft(電流))[0:len(電流)//2]
    頻率 = np.fft.fftfreq(len(時間), 時間[1] - 時間[0])[0:len(時間)//2]
    軸2.plot(頻率, 電壓傅立葉, 'b-', label='電壓頻譜')
    軸2.plot(頻率, 電流傅立葉, 'r--', label='電流頻譜')
    軸2.set_xlabel('頻率 (Hz)', fontproperties=font)
    軸2.set_ylabel('幅度', fontproperties=font)
    軸2.set_title('頻域譜', fontproperties=font)
    軸2.set_xlim(0, 0.5)
    軸2.grid(True)
    軸2.legend()
    
    plt.tight_layout()
    plt.savefig('voltage_current.png', dpi=300)
    plt.close()

# 圖 2: 傅立葉分解水位波浪與頻率成分
def 繪製方波傅立葉():
    方波 = signal.square(2 * np.pi * 方波時間)
    傅立葉 = np.fft.fft(方波)
    頻率 = np.fft.fftfreq(len(方波時間), 方波時間[1] - 方波時間[0])
    正頻率 = 頻率 > 0
    頻率 = 頻率[正頻率]
    傅立葉幅度 = np.abs(傅立葉)[正頻率]
    
    圖表, (軸1, 軸2) = plt.subplots(2, 1, figsize=(8, 6))
    軸1.plot(方波時間, 方波, 'b-', label='方波 (水位波浪)')
    軸1.set_xlabel('時間 (秒)', fontproperties=font)
    軸1.set_ylabel('振幅', fontproperties=font)
    軸1.set_title('時域方波', fontproperties=font)
    軸1.grid(True)
    軸1.legend()
    
    軸2.stem(頻率, 傅立葉幅度, 'b', label='頻率成分')
    軸2.set_xlabel('頻率 (Hz)', fontproperties=font)
    軸2.set_ylabel('幅度', fontproperties=font)
    軸2.set_title('頻域譜 (奇次諧波)', fontproperties=font)
    軸2.grid(True)
    軸2.legend()
    軸2.text(0.5, max(傅立葉幅度) * 0.9, '與量子能級相關 (圖 6)', fontsize=8, fontproperties=font)
    
    plt.tight_layout()
    plt.savefig('square_wave_fft.png', dpi=300)
    plt.close()

# 圖 3: 尤拉公式與相位旋轉動畫
def 繪製單位圓動畫():
    圖表, 軸 = plt.subplots(figsize=(8, 8))
    θ = np.linspace(0, 2 * np.pi, 100)
    軸.plot(np.cos(θ), np.sin(θ), 'k-', label='單位圓')
    軸.axhline(0, color='k', alpha=0.3); 軸.axvline(0, color='k', alpha=0.3)
    
    # 初始向量
    初始時間 = np.pi / 4
    電壓向量, = 軸.plot([0, np.cos(ω * 初始時間)], [0, np.sin(ω * 初始時間)], 'b-', lw=2, label=r'電壓 $\cos(\omega t)$')
    電流向量, = 軸.plot([0, np.sin(ω * 初始時間)], [0, np.cos(ω * 初始時間)], 'r--', lw=2, label=r'電流 $\sin(\omega t)$')
    量子向量, = 軸.plot([0, 0.5 * np.cos(ω * 初始時間 + np.pi/4)], [0, 0.5 * np.sin(ω * 初始時間 + np.pi/4)],
                         'c-', lw=2, label=r'量子 ($45^\circ$ 起始)')
    
    # 插圖：儲水池類比
    插圖軸 = 軸.inset_axes([0.1, 0.1, 0.3, 0.3])
    插圖時間 = np.linspace(0, 2 * np.pi, 100)
    插圖軸.plot(插圖時間, np.cos(插圖時間), 'b-', label='水位')
    插圖軸.arrow(np.pi/4, 0, 0, 1, head_width=0.1, head_length=0.2, fc='r', ec='r', label='流量')
    插圖軸.set_title('儲水池類比', fontsize=8, fontproperties=font)
    插圖軸.set_xticks([]); 插圖軸.set_yticks([])
    插圖軸.text(0.1, 1.0, r'流量領先 $\pi/2$', fontsize=8, fontproperties=font)
    
    軸.set_xlabel('實部', fontproperties=font)
    軸.set_ylabel('虛部', fontproperties=font)
    軸.set_title(r'尤拉公式: $e^{j\theta} = \cos(\theta) + j \sin(\theta)$', fontproperties=font)
    軸.set_xlim(-1.5, 1.5); 軸.set_ylim(-1.5, 1.5)
    軸.grid(True)
    軸.legend()
    軸.text(0.1, 1.3, '電流比電壓領先 90°。\n量子相位從 45° 開始並演化。', fontsize=10, fontproperties=font)
    
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
        幀列表 = np.arange(0, 2 * np.pi, 0.1)
        print(f"正在為動畫生成 {len(幀列表)} 幀")
        for i, 幀 in enumerate(幀列表):
            更新(幀)
            圖表.canvas.draw()
            plt.savefig(os.path.join(臨時幀目錄, f'frame_{i:04d}.png'), dpi=300)
        
        幀檔案 = sorted(glob.glob(os.path.join(臨時幀目錄, 'frame_*.png')))
        print(f"正在將 {len(幀檔案)} 幀合併為 GIF")
        圖像列表 = [Image.open(幀檔案路徑) for 幀檔案路徑 in 幀檔案]
        圖像列表[0].save(
            最終GIF,
            save_all=True,
            append_images=圖像列表[1:],
            duration=50,  # 每幀 50 毫秒 (20 fps)
            loop=0  # 無限循環
        )
        
        for 幀檔案路徑 in 幀檔案:
            os.remove(幀檔案路徑)
        os.rmdir(臨時幀目錄)
        
    except Exception as e:
        print(f"動畫生成過程中發生錯誤: {e}")
    finally:
        plt.close()

# 圖 4: LC共振 vs 場模態能量分布
def 繪製LC共振():
    頻率 = np.linspace(0.01, 0.5, 1000)  # 頻率 (Hz)
    共振頻率 = 1 / (2 * np.pi * np.sqrt(電感 * 電容))  # f_0 = 1/(2π√LC)
    阻抗 = np.abs(1j * 2 * np.pi * 頻率 * 電感 + 1 / (1j * 2 * np.pi * 頻率 * 電容))
    電流幅度 = 1 / 阻抗  # 假設輸入電壓 = 1V
    
    # 量子場模態
    模態 = np.arange(0, 5)  # 模態 n = 0, 1, 2, ...
    模態能量 = ℏ * 2 * np.pi * 共振頻率 * (模態 + 0.5)  # E_n = ℏω (n + 1/2)
    
    圖表, (軸1, 軸2) = plt.subplots(2, 1, figsize=(8, 6))
    # LC 共振
    軸1.plot(頻率, 電流幅度, 'b-', label=r'電流幅度 $I = 1/|Z|$')
    軸1.axvline(共振頻率, color='k', linestyle=':', label=r'$f_0 = \frac{1}{2\pi \sqrt{LC}}$')
    軸1.set_xlabel('頻率 (Hz)', fontproperties=font)
    軸1.set_ylabel('電流幅度 (A)', fontproperties=font)
    軸1.set_title('LC 共振', fontproperties=font)
    軸1.grid(True)
    軸1.legend()
    
    # 場模態
    軸2.stem(模態, 模態能量, 'b', label=r'能量 $E_n = \hbar \omega (n + \frac{1}{2})$')
    軸2.set_xlabel('模態 $n$', fontproperties=font)
    軸2.set_ylabel('能量 (J)', fontproperties=font)
    軸2.set_title('量子場模態能量分布', fontproperties=font)
    軸2.grid(True)
    軸2.legend()
    
    plt.tight_layout()
    plt.savefig('lc_resonance.png', dpi=300)
    plt.close()

# 圖 5: 量子場 vs 電路場完整對照圖（表格形式）
def 繪製量子電路對照():
    圖表, 軸 = plt.subplots(figsize=(10, 6))
    軸.axis('off')
    
    # 表格數據
    欄位 = ['物理量', '電路場描述', '量子場描述']
    數據 = [
        ['電壓', r'$V(t) = V_0 \cos(\omega t)$', r'$\psi \sim e^{-j E t / \hbar}$ (相位演化)'],
        ['電流', r'$I(t) = C \frac{dV}{dt}$', r'光子流 $\propto \hat{a}^\dagger \hat{a}$'],
        ['能量', r'$E = \frac{1}{2} C V^2 + \frac{1}{2} L I^2$', r'$E_n = \hbar \omega (n + \frac{1}{2})$'],
        ['共振頻率', r'$f_0 = \frac{1}{2\pi \sqrt{LC}}$', r'模態頻率 $\omega$']
    ]
    
    表格 = 軸.table(cellText=數據, colLabels=欄位, loc='center', cellLoc='center')
    表格.auto_set_font_size(False)
    表格.set_fontsize(10)
    表格.scale(1.2, 1.5)
    
    軸.set_title('量子場 vs 電路場對照表', fontproperties=font)
    plt.tight_layout()
    plt.savefig('quantum_circuit_table.png', dpi=300)
    plt.close()

# 圖 6: 超導量子比特與能階結構示意圖
def 繪製超導量子比特():
    量子比特頻率 = 2 * np.pi * 5e9  # 5 GHz
    模態 = np.arange(0, 4)  # 能級 n = 0, 1, 2, 3
    能級 = ℏ * 量子比特頻率 * (模態 + 0.5)  # E_n = ℏω (n + 1/2)
    
    圖表, 軸 = plt.subplots(figsize=(8, 6))
    for n, E in enumerate(能級):
        軸.axhline(E, color='b', linestyle='-', xmin=0.2, xmax=0.8)
        軸.text(0.85, E, f'$|{n}\\rangle$', fontsize=12, verticalalignment='center')
    軸.arrow(0.5, 能級[0], 0, 能級[1] - 能級[0], head_width=0.02, head_length=0.1e-24, fc='r', ec='r')
    軸.text(0.55, (能級[0] + 能級[1]) / 2, r'$\omega_{01}$', fontsize=10, color='r')
    
    軸.set_xlim(0, 1)
    軸.set_ylim(-0.5e-24, 能級[-1] * 1.2)
    軸.set_xlabel('示意軸', fontproperties=font)
    軸.set_ylabel('能量 (J)', fontproperties=font)
    軸.set_title('超導量子比特能階結構', fontproperties=font)
    軸.grid(True, axis='y')
    
    # 插圖：簡化超導電路
    插圖軸 = 軸.inset_axes([0.1, 0.65, 0.25, 0.25])  # 調整位置和大小
    插圖軸.plot([0, 1], [0, 0], 'k-', lw=2)  # 電路線
    插圖軸.text(0.5, 0.05, '約瑟夫森結', fontsize=7, fontproperties=font, ha='center')
    插圖軸.set_xlim(-0.2, 1.2)
    插圖軸.set_ylim(-0.2, 0.3)
    插圖軸.set_xticks([]); 插圖軸.set_yticks([])
    插圖軸.set_title('超導電路', fontsize=7, fontproperties=font)
    
    軸.text(0.1, 能級[-1] * 1.2, '用於量子計算的離散能級', fontsize=9, fontproperties=font)
    
    plt.tight_layout(pad=2.0, h_pad=2.0, w_pad=2.0)
    plt.savefig('superconducting_qubit.png', dpi=300)
    plt.close()

# 主函數：生成所有圖表
def 主程式():
    繪製電壓電流()          # 圖 1
    繪製方波傅立葉()        # 圖 2
    繪製單位圓動畫()        # 圖 3
    繪製LC共振()            # 圖 4
    繪製量子電路對照()      # 圖 5
    繪製超導量子比特()      # 圖 6
    print("所有圖表生成成功：voltage_current.png, square_wave_fft.png, euler_animation.gif, lc_resonance.png, quantum_circuit_table.png, superconducting_qubit.png")

if __name__ == "__main__":
    主程式()
