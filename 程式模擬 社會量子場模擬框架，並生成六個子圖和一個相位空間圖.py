import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 設定中文字體以避免字形缺失警告
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'sans-serif']  # 優先使用 Microsoft YaHei
plt.rcParams['axes.unicode_minus'] = False  # 確保負號正確顯示

# 參數設定
N = 100  # 空間格點數量
L = 10.0  # 空間範圍大小
dx = L / N  # 空間格點間距
dt = 0.01  # 時間步長
T = 1000  # 時間步數
m_yijian, m_jingji = 1.0, 1.0  # 場的質量（社會變量的慣性）
lam, eta = 0.1, 0.1  # 自耦合常數（自我增強）
g = 0.5  # 場間耦合常數（相互依賴）
chuangkou_daxiao = 10  # 糾纏近似窗口大小

# 社會解釋參數
yijian_biaoqian = "意見強度"  # yijian 表示政治意見（-1：自由派，+1：保守派）
jingji_biaoqian = "經濟情緒"  # jingji 表示經濟樂觀/悲觀（-1：悲觀，+1：樂觀）
quyu_biaoqian = "社會區域"  # 空間格點表示地理或網絡區域

# 局部能量密度函數（僅針對 yijian，聚焦於意見動態）
def jubu_nengliang_midu(yijian, shiliang, dx, m_yijian, lam):
    """
    計算 yijian 場的局部能量密度，表示社會活動（如意見強度）。
    輸入：
        yijian：場值（意見強度）
        shiliang：共軛動量（意見變化率）
        dx：空間格點間距
        m_yijian：質量參數（慣性）
        lam：自耦合（自我增強）
    輸出：
        nengliang：能量密度陣列
    """
    yijian_tidu = (np.roll(yijian, -1) - np.roll(yijian, 1)) / (2 * dx)  # 週期中心差分
    nengliang = 0.5 * shiliang**2 + 0.5 * yijian_tidu**2 + 0.5 * m_yijian**2 * yijian**2 + 0.25 * lam * yijian**4
    return nengliang

# 初始化場
x = np.linspace(0, L, N, endpoint=False)
yijian, jingji = np.zeros(N), np.zeros(N)
shiliang_yijian, shiliang_jingji = np.zeros(N), np.zeros(N)
yijian = np.exp(-(x - L/2)**2 / 0.5)  # 中央區域初始意見激增
jingji = 0.1 * np.sin(2 * np.pi * x / L)  # 經濟情緒初始振盪

# 儲存分析數據
yijian_lishi = [yijian.copy()]  # 儲存 yijian 快照用於視覺化
jingji_lishi = [jingji.copy()]  # 儲存 jingji 快照
zhenkong_qiwang_yijian = [np.mean(yijian)]  # yijian 的真空期望值（平均意見）
zhenkong_qiwang_jingji = [np.mean(jingji)]  # jingji 的真空期望值（平均經濟情緒）
jiuchan_jinsi = []  # 平均相關性（社會連通性）
nengliang_zonghe = []  # 總能量（社會活動水平）
xiangwei_kongjian = [(yijian.copy(), shiliang_yijian.copy())]  # 儲存 (yijian, shiliang_yijian) 用於相位空間

# 時間演化
for t in range(T):
    # 計算拉普拉斯算子（社會變量的空間擴散）
    lap_yijian = (np.roll(yijian, -1) - 2 * yijian + np.roll(yijian, 1)) / dx**2
    lap_jingji = (np.roll(jingji, -1) - 2 * jingji + np.roll(jingji, 1)) / dx**2
    
    # 運動方程（包含自我增強和耦合的社會動態）
    d2_yijian = lap_yijian - m_yijian**2 * yijian - lam * yijian**3 + 2 * g * yijian * jingji
    d2_jingji = lap_jingji - m_jingji**2 * jingji - eta * jingji**3 + g * yijian**2
    
    # 蛙跳法更新
    shiliang_yijian += dt * d2_yijian
    shiliang_jingji += dt * d2_jingji
    yijian += dt * shiliang_yijian
    jingji += dt * shiliang_jingji
    
    # 每 200 步儲存一次數據
    if t % 200 == 0:
        yijian_lishi.append(yijian.copy())
        jingji_lishi.append(jingji.copy())
        xiangwei_kongjian.append((yijian.copy(), shiliang_yijian.copy()))
    
    # 計算真空期望值（社會規範）
    zhenkong_qiwang_yijian.append(np.mean(yijian))
    zhenkong_qiwang_jingji.append(np.mean(jingji))
    
    # 計算總能量（社會活動水平）
    yijian_tidu = (np.roll(yijian, -1) - np.roll(yijian, 1)) / (2 * dx)
    jingji_tidu = (np.roll(jingji, -1) - np.roll(jingji, 1)) / (2 * dx)
    shijian = (0.5 * m_yijian**2 * yijian**2 + 0.5 * m_jingji**2 * jingji**2 + 
               0.25 * lam * yijian**4 + 0.25 * eta * jingji**4 - g * yijian**2 * jingji)
    nengliang = (0.5 * shiliang_yijian**2 + 0.5 * shiliang_jingji**2 + 
                 0.5 * yijian_tidu**2 + 0.5 * jingji_tidu**2 + shijian).sum() * dx
    nengliang_zonghe.append(nengliang)
    
    # 糾纏近似（社會連通性）
    jiuchan_jinsi_list = []
    for i in range(len(yijian) - chuangkou_daxiao):
        A = jubu_nengliang_midu(yijian[i:i+chuangkou_daxiao], shiliang_yijian[i:i+chuangkou_daxiao], dx, m_yijian, lam)
        B = jubu_nengliang_midu(yijian[i+1:i+1+chuangkou_daxiao], shiliang_yijian[i+1:i+1+chuangkou_daxiao], dx, m_yijian, lam)
        if np.std(A) > 1e-10 and np.std(B) > 1e-10:
            xiangguan = np.corrcoef(A, B)[0, 1]
        else:
            xiangguan = 0.0
        jiuchan_jinsi_list.append(xiangguan)
    jiuchan_jinsi.append(np.mean(jiuchan_jinsi_list))

# 空間相關性分佈（社會影響範圍）
juli = np.arange(1, N - chuangkou_daxiao + 1, 10)  # 確保 d + chuangkou_daxiao <= N
xiangguan_list = []
for d in juli:
    A = jubu_nengliang_midu(yijian[0:chuangkou_daxiao], shiliang_yijian[0:chuangkou_daxiao], dx, m_yijian, lam)
    B = jubu_nengliang_midu(yijian[d:d+chuangkou_daxiao], shiliang_yijian[d:d+chuangkou_daxiao], dx, m_yijian, lam)
    if np.std(A) > 1e-10 and np.std(B) > 1e-10:
        xiangguan_list.append(np.corrcoef(A, B)[0, 1])
    else:
        xiangguan_list.append(0.0)

# 視覺化（調整佈局以防止文字重疊）
plt.figure(figsize=(15, 12))

# 調整子圖間距
plt.subplots_adjust(hspace=0.4, wspace=0.3)  # 增加垂直和水平間距

# 子圖 1：意見動態（yijian 演化，對稱性破缺）
plt.subplot(3, 2, 1)
for i, yijian_kuaizhao in enumerate(yijian_lishi):
    plt.plot(x, yijian_kuaizhao, label=f'時間={i*200*dt:.1f}')
plt.xlabel(quyu_biaoqian, fontsize=10)
plt.ylabel(yijian_biaoqian, fontsize=10)
plt.title(f'{yijian_biaoqian}動態（極化）', fontsize=11, pad=10)
plt.legend(fontsize=8, loc='upper right', bbox_to_anchor=(1.15, 1.0))

# 子圖 2：經濟情緒動態（jingji 演化）
plt.subplot(3, 2, 2)
for i, jingji_kuaizhao in enumerate(jingji_lishi):
    plt.plot(x, jingji_kuaizhao, label=f'時間={i*200*dt:.1f}')
plt.xlabel(quyu_biaoqian, fontsize=10)
plt.ylabel(jingji_biaoqian, fontsize=10)
plt.title(f'{jingji_biaoqian}動態', fontsize=11, pad=10)
plt.legend(fontsize=8, loc='upper right', bbox_to_anchor=(1.15, 1.0))

# 子圖 3：真空期望值（社會規範）
plt.subplot(3, 2, 3)
plt.plot(np.arange(T+1) * dt, zhenkong_qiwang_yijian, label=f'平均{yijian_biaoqian}')
plt.plot(np.arange(T+1) * dt, zhenkong_qiwang_jingji, label=f'平均{jingji_biaoqian}')
plt.xlabel('時間', fontsize=10)
plt.ylabel('平均值', fontsize=10)
plt.title('社會規範（真空期望值）', fontsize=11, pad=10)
plt.legend(fontsize=8, loc='upper right')

# 子圖 4：糾纏（社會連通性）
plt.subplot(3, 2, 4)
plt.plot(np.arange(T) * dt, jiuchan_jinsi)
plt.xlabel('時間', fontsize=10)
plt.ylabel('平均相關性', fontsize=10)
plt.title('社會連通性（糾纏）', fontsize=11, pad=10)

# 子圖 5：能量（社會活動穩定性）
plt.subplot(3, 2, 5)
plt.plot(np.arange(T) * dt, nengliang_zonghe)
plt.xlabel('時間', fontsize=10)
plt.ylabel('總社會活動', fontsize=10)
plt.title('活動穩定性', fontsize=11, pad=10)

# 子圖 6：空間相關性分佈（影響範圍）
plt.subplot(3, 2, 6)
plt.plot(juli * dx, xiangguan_list)
plt.xlabel('距離', fontsize=10)
plt.ylabel('相關性', fontsize=10)
plt.title('空間相關性分佈', fontsize=11, pad=10)

# 應用緊湊佈局並增加額外間距
plt.tight_layout(pad=2.0)

# 顯示圖表
plt.show()

# 相位空間圖（混沌動態）
plt.figure(figsize=(8, 6))
for yijian_kuaizhao, shiliang_kuaizhao in xiangwei_kongjian[::2]:  # 每隔一個快照繪製
    plt.scatter(yijian_kuaizhao[::10], shiliang_kuaizhao[::10], s=5, alpha=0.5)
plt.xlabel(yijian_biaoqian, fontsize=10)
plt.ylabel(f'{yijian_biaoqian}變化率', fontsize=10)
plt.title('相位空間（混沌動態）', fontsize=11, pad=10)
plt.tight_layout(pad=2.0)
plt.show()
