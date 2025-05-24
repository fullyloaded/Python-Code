import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class RealTimeDataStream:
    def __init__(self, data_length=100):
        self.data_length = data_length
        self.current_index = 0

    def get_next_data(self):
        # 模擬隨機即時資料（可替換成真實資料串流）
        data = np.sin(0.1 * self.current_index) + np.random.normal(scale=0.1)
        self.current_index += 1
        return data

class SimpleAIModel:
    def __init__(self):
        self.weight = 0.5  # 簡單權重

    def predict(self, x):
        # 簡單線性預測
        return self.weight * x

    def update(self, x, y_true):
        # 簡單梯度下降更新權重
        y_pred = self.predict(x)
        grad = (y_pred - y_true) * x
        lr = 0.01
        self.weight -= lr * grad

class PredictiveField:
    def __init__(self):
        self.field_state = 0.0

    def update_field(self, prediction, data):
        # 利用預測結果與資料更新場的狀態
        self.field_state = 0.8 * self.field_state + 0.2 * (prediction + data) / 2

def main_simulation(steps=100):
    # 初始化模擬物件
    data_stream = RealTimeDataStream()
    model = SimpleAIModel()
    field = PredictiveField()

    # 初始化數據儲存
    data_history = []
    pred_history = []
    field_history = []
    step_history = []

    # 設定圖表
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.set_facecolor('white')  # 白色背景
    ax.set_xlim(0, steps)
    ax.set_ylim(-1.5, 1.5)  # 根據數據範圍設置
    ax.set_xlabel('Step')
    ax.set_ylabel('Value')
    ax.set_title('Real-Time Data Stream Simulation')
    ax.grid(True)

    # 初始化折線
    line_data, = ax.plot([], [], 'b-', label='Data', linewidth=2)
    line_pred, = ax.plot([], [], 'r-', label='Prediction', linewidth=2)
    line_field, = ax.plot([], [], 'g-', label='Field State', linewidth=2)
    ax.legend(loc='upper left')

    def update(frame):
        # 獲取新數據
        data = data_stream.get_next_data()
        prediction = model.predict(data)
        field.update_field(prediction, data)
        model.update(data, data)

        # 儲存歷史數據
        step_history.append(frame)
        data_history.append(data)
        pred_history.append(prediction)
        field_history.append(field.field_state)

        # 更新折線數據
        line_data.set_data(step_history, data_history)
        line_pred.set_data(step_history, pred_history)
        line_field.set_data(step_history, field_history)

        # 動態調整 X 軸範圍
        if frame > steps // 2:
            ax.set_xlim(frame - steps // 2, frame + steps // 2)

        # 輸出當前狀態
        print(f"Step {frame:3d} | Data: {data:.3f} | Prediction: {prediction:.3f} | Field State: {field.field_state:.3f}")

        return line_data, line_pred, line_field

    # 生成動畫
    ani = FuncAnimation(fig, update, frames=steps, interval=100, blit=True)

    # 保存動畫為 MP4（需要 FFmpeg）並顯示
    ani.save('realtime_simulation.mp4', writer='ffmpeg', dpi=100)
    plt.show()

if __name__ == "__main__":
    main_simulation()
