# 🍽️ 校园食堂美食测评系统

基于 Python + Streamlit + Pandas + Matplotlib 开发的校园食堂美食测评系统。

## ✨ 功能特性

| 功能模块 | 状态 | 负责人 |
|----------|------|--------|
| 菜品录入&打分 | ✅ 已实现 | A同学 |
| 菜品检索查询 | ✅ 已实现 | A同学 |
| 热度排行 | ⏳ 待开发 | B同学 |
| 数据可视化 | ⏳ 待开发 | B同学 |
| 智能饮食推荐 | ⏳ 待开发 | B同学 |

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip 包管理器

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone <仓库地址>
   cd campus_food
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行应用**
   ```bash
   streamlit run main.py
   ```

4. **访问应用**
   
   浏览器会自动打开，或手动访问：`http://localhost:8501`

## 📁 项目结构

```
campus_food/
├── .git/                  # Git仓库
├── .gitignore            # Git忽略配置
├── README.md             # 项目说明文档
├── requirements.txt      # Python依赖
├── main.py               # 主程序文件
└── food_data.csv         # 数据存储文件
```

## 🎯 功能说明

### 菜品录入&打分（A同学负责）
- 食堂名称、菜品名称文本输入
- 口味分类下拉选择（减脂、清淡、重口、香辣、甜口）
- 价格数字输入（支持小数）
- 评分滑动选择器（1-5分）
- 多行评论输入
- 表单验证与提交成功提示

### 菜品检索查询（A同学负责）
- 食堂名称关键词搜索
- 菜品名称关键词搜索
- 口味分类筛选
- 评分范围筛选（1-5分）
- 价格范围筛选
- 搜索结果表格展示
- 菜品详情展开查看

### 待开发功能（B同学负责）
- 热度排行
- 数据可视化（饼图、柱状图等）
- 智能饮食推荐

## 📊 数据结构

| 字段 | 类型 | 说明 |
|------|------|------|
| 食堂名称 | 字符串 | 食堂名称 |
| 菜品名称 | 字符串 | 菜品名称 |
| 口味分类 | 字符串 | 减脂/清淡/重口/香辣/甜口 |
| 价格 | 浮点数 | 菜品价格（元） |
| 评分 | 整数 | 1-5分 |
| 评论 | 字符串 | 菜品评价 |
| 录入时间 | 字符串 | 提交时间 |

## 📝 Git 协作规范

### 分支管理

```
main                # 主分支（稳定版本）
└── feature-add-food # A同学：菜品录入模块
└── feature-search   # B同学：菜品检索模块
└── feature-ranking  # B同学：热度排行模块
└── feature-visual   # B同学：数据可视化模块
└── feature-recommend # B同学：智能推荐模块
```

### 提交信息格式

```
<类型>：<描述>

详细说明（可选）
```

**常用类型：**

- `[Feature]` 新增功能
- `[Fix]` 修复问题
- `[Doc]` 更新文档
- `[Config]` 配置变更

**示例：**
```bash
git commit -m "[Feature] 实现菜品录入打分功能"
git commit -m "[Fix] 修复表单验证逻辑"
```

### 常用 Git 命令

```bash
# 拉取最新代码
git pull origin main

# 创建特性分支
git checkout -b feature-add-food

# 添加文件
git add .

# 提交变更
git commit -m "[Feature] 描述信息"

# 推送分支
git push origin feature-add-food
```

## 🔧 开发计划

| 阶段 | 任务 | 负责人 |
|------|------|--------|
| 第一阶段 | 公共基础代码 + 菜品录入打分 + 菜品检索查询 | A同学 |
| 第二阶段 | 热度排行 | B同学 |
| 第三阶段 | 数据可视化 + 智能推荐 | B同学 |

## 📄 许可证

本项目仅供学习交流使用。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**项目名称**：校园食堂美食测评系统  
**技术栈**：Python + Streamlit + Pandas + Matplotlib  
**运行命令**：streamlit run main.py
