Taiwan Influence Dynamics Simulation
概述
Taiwan Influence Dynamics Simulation 是一個基於 React 和 D3.js 的互動式動畫工具，用於模擬台灣在中美影響力競爭中的地緣政治動態。該程式通過彩色粒子和真空泡泡（vacuum bubbles）視覺化美國（φ₁）、中國（φ₂）、台灣（φ₃）以及其他國際行為者（φ₄，如日本、歐盟）之間的影響力流動與競爭。模擬包括正常狀態（影響力平衡流動）和危機狀態（台海緊張導致影響力撤離），並支持 10 秒動畫錄製功能（WebM 格式）。
功能特點
	•	動態粒子模擬：彩色粒子代表影響力（政治、經濟、軍事、文化），根據領域的吸引/排斥力移動。
	•	領域互動：
	◦	中美競爭：美國與中國對台灣的影響力競爭激烈。
	◦	美國與其他國際行為者合作：模擬台美日聯盟等合作關係。
	◦	中國與其他國際行為者競爭：反映地緣政治分歧。
	•	正常狀態：台灣在中美之間維持影響力平衡。
	•	危機狀態：模擬台海緊張（如軍事衝突或經濟制裁），台灣穩定性下降，影響力撤離，生成真空泡泡。
	•	視訊匯出：錄製 10 秒動畫，生成 WebM 格式視訊以展示影響力動態。
	•	量子場論靈感：粒子運動類比量子場論中的場激發，真空泡泡反映場的不穩定性。
安裝
先決條件
	•	Node.js：版本 16 或以上
	•	npm 或 yarn：用於安裝依賴
	•	現代瀏覽器：推薦 Chrome 或 Firefox（支援 Canvas 錄製）
安裝步驟
	1	克隆儲存庫： git clone 
	2	cd taiwan-influence-simulation
	3	
	4	安裝依賴： npm install
	5	 或 yarn install
	6	
	7	安裝 D3.js 和其他依賴： 確保在 package.json 中包含以下依賴： "dependencies": {
	8	  "react": "^18.2.0",
	9	  "react-dom": "^18.2.0",
	10	  "d3": "^7.8.5"
	11	}
	12	
	13	啟動開發伺服器： npm start
	14	 或 yarn start
	15	 應用程式將在 http://localhost:3000 運行。
使用方法
	1	啟動動畫：
	◦	點擊「Start Animation」按鈕開始模擬，觀察影響力粒子在美國、中國、台灣和其他國際行為者之間的流動。
	◦	點擊「Pause Animation」暫停動畫。
	2	觸發危機：
	◦	點擊「Trigger φ₃ Crisis」模擬台海緊張（如軍事演習或經濟制裁）。台灣領域（φ₃）將變為紅色並震盪，綠色粒子被排斥，生成真空泡泡。
	◦	再次點擊「Stop φ₃ Crisis」恢復正常狀態。
	3	錄製視訊：
	◦	點擊「Export Video (10s)」錄製 10 秒動畫，自動下載為 WebM 格式。
	◦	建議在危機狀態下錄製以捕捉完整動態。
	◦	點擊「Stop Recording」提前結束錄製。
	4	觀察互動：
	◦	藍色粒子：美國影響力（如軍售、貿易協定）。
	◦	橙色粒子：中國影響力（如經濟壓力、兩岸貿易）。
	◦	綠色粒子：台灣影響力（如高科技、民主價值）。
	◦	紅色粒子：其他國際行為者影響力（如日本技術合作、歐盟經貿支持）。
技術細節
程式結構
	•	React：用於構建使用者介面，管理動畫狀態（isPlaying、crisis、isRecording）。
	•	D3.js：用於 SVG 渲染，處理粒子運動與領域互動。
	•	Canvas API：用於錄製動畫，轉換 SVG 為 WebM 視訊。
	•	Tailwind CSS：提供響應式樣式與視覺設計。
領域定義
	•	φ₁ - 美國：穩定性 0.9（正常）/1.0（危機），提供軍事與經濟支持，與其他國際行為者合作。
	•	φ₂ - 中國：穩定性 0.9（正常）/1.0（危機），施加經濟與外交壓力，與其他國際行為者競爭。
	•	φ₃ - 台灣：穩定性 0.7（正常）/0.3（危機），中美競爭焦點，危機時影響力撤離。
	•	φ₄ - 其他國際行為者：穩定性 0.6（正常）/0.7（危機），包括日本、歐盟，與美國合作。
動畫邏輯
	•	正常狀態：粒子根據領域穩定性（stability）受吸引，模擬影響力平衡。美國與中國競爭（相反吸引力），美國與其他國際行為者合作（弱吸引力）。
	•	危機狀態：台灣穩定性降至 0.3，生成排斥力，綠色粒子撤離，隨機產生真空泡泡（紅色邊框圓圈）。美國與中國吸引力增強，吸收部分影響力。
	•	粒子運動：每個粒子具有位置（x, y）、速度（vx, vy）、半徑（radius）與生命週期（life），根據物理模擬更新。
	•	真空泡泡：模擬影響力真空，危機時隨機生成，隨時間擴展並消失。
程式碼片段
// 粒子互動邏輯（簡化）
particles.forEach(p => {
  fields.forEach((field, index) => {
    const dx = field.x - p.x;
    const dy = field.y - p.y;
    const dist = Math.sqrt(dx * dx + dy * dy);
    if (dist < field.baseRadius * 2) {
      const force = (field.stability * 0.02) / (dist + 1);
      p.vx += dx * force;
      p.vy += dy * force;
    }
    // 中美競爭
    if (index === 0) { // 美國
      const cnField = fields[1];
      const cnDist = Math.sqrt((cnField.x - p.x) ** 2 + (cnField.y - p.y) ** 2);
      if (cnDist < cnField.baseRadius * 2) {
        p.vx -= (cnField.x - p.x) * (0.015 / (cnDist + 1));
        p.vy -= (cnField.y - p.y) * (0.015 / (cnDist + 1));
      }
    }
    // 危機狀態：台灣不穩定
    if (crisis && index === 2) {
      if (dist < field.baseRadius * 3) {
        const repulsion = 0.6 / (dist + 1);
        p.vx -= dx * repulsion;
        p.vy -= dy * repulsion;
        if (Math.random() < 0.06) {
          createVacuumBubble(p.x, p.y, 1.8);
        }
      }
    }
  });
});
未來改進
	•	特定事件模擬：新增按鈕觸發具體事件（如「中國軍演」或「美國軍售」），調整粒子行為。
	•	粒子數量調整：允許用戶動態改變粒子數量或速度，增強互動性。
	•	數據驅動：整合真實數據（如台灣進出口數據或外交事件），驅動粒子分佈。
	•	視覺增強：添加粒子軌跡線或影響力強度熱圖。
	•	多語言支持：將 UI 翻譯為繁體中文或其他語言，適應台灣本地用戶。
注意事項
	•	瀏覽器相容性：錄製功能需 Chrome 或 Firefox，IE 或舊版瀏覽器可能不支援。
	•	效能：粒子數量過多（>200）可能影響效能，建議保持 100 個粒子。
	•	視訊格式：WebM 格式可用 VLC 播放，或使用線上工具轉換為 MP4/GIF。
貢獻
歡迎提交問題或拉取請求！請遵循以下步驟：
	1	Fork 儲存庫。
	2	創建功能分支（git checkout -b feature/new-feature）。
	3	提交更改（git commit -m 'Add new feature'）。
	4	推送到分支（git push origin feature/new-feature）。
	5	開啟拉取請求。
許可證
本項目採用 MIT 許可證。詳情見 LICENSE。
聯繫
如有問題，請提交 GitHub Issue。
這個 README.md 提供了清晰的項目概述，涵蓋了台灣情境的模擬邏輯、技術實現與使用指南。如果需要調整內容（例如添加具體事件模擬、繁體中文版本或更詳細的技術說明），請告訴我，我可以進一步優化！
