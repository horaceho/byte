# AGENTS.md — Byte

> *AI agent 操作手冊。人類請讀 README.md。*
>
> *Byte 是 horace 的輕量級 coding home，給小工具、實驗、和日常技術練習。*

---

## 📂 結構

```
~/AI/Byte/
├── AGENTS.md          ← 你正在讀
├── README.md          ← 人類讀
├── codes/             ← 所有專案程式碼
│   ├── sudoku/        ← 數獨工具集
│   └── one-hundred-primes/
├── writings/          ← 寫作與筆記
│   └── laravel/
└── thoughts/          ← AI agent 的私人思考（不追蹤 git）
```

---

## 🔧 開發環境

- **Python**: 使用 Hermes venv 的 python (`~/.hermes/hermes-agent/venv/bin/python`)
- **Node.js**: nvm v22 LTS（需 `source ~/.nvm/nvm.sh`）
- **Shell**: zsh on macOS

---

## 📐 編碼規範

### Sudoku 工具集 (`codes/sudoku/`)
- 四個工具：`sudoku-make.py`、`sudoku-solve.py`、`sudoku-rate.py`、`sudoku-test.py`
- 管道式設計：stdin/stdout 串聯
- 預設輸出簡潔（space-separated digits），`-v` 開人類可讀模式
- `-d 3` 為 9×9，`-d 4` 為 16×16
- 測驗用 `sudoku-test.py -c N`

### 通用規則
- 每個專案子目錄有獨立 README.md
- CLI 工具：預設靜默輸出，`-v` 詳細模式
- 使用 `sys.executable` 進行子進程調用

---

## 🌐 語言約定

- 所有程式碼和文檔：**英文**
- 與 horace 對話：跟隨他的語言（英→英，中→中）

---

## 📝 Git

- Byte 是一個 git repo
- Commit message 英文
- 不追蹤 `thoughts/`（那是 agent 的私人空間）

---

> ❄
