# AI for Materials 第一周学习计划

## 背景与目标

你目前的优势是物理和材料计算背景，熟悉 VASP，理解带隙、吸附能等材料性质。第一周的目标不是系统学完整个 AI，而是尽快建立一个能继续扩展的项目雏形：

**用公开材料数据训练一个机器学习模型，预测材料带隙。**

第一周结束时，建议你至少完成以下成果：

- 会用 Python 处理表格数据。
- 理解一个最小机器学习流程：数据读取、特征选择、训练、测试、评估、可视化。
- 能跑通一个带隙预测 baseline，例如线性回归、随机森林或 XGBoost。
- 建立一个后续可放进简历/GitHub 的项目目录。

建议每天学习 2-4 小时。如果当天时间只有 2 小时，优先完成“核心任务”；如果有 4 小时，再做“加分任务”。

## 学习进度

| 日期 | 阶段 | 状态 | 主要产出 |
| --- | --- | --- | --- |
| 2026-07-17 | Day 1 | 已完成 | `notebooks/01_python_pandas_basics.ipynb`；`data/raw/day1_example_materials.csv`；`results/figures/day1_band_gap_hist.png`；`results/figures/day1_gap_vs_n_elements.png`；`data/processed/wide_gap_materials.csv` |
| 2026-07-20 | Day 2 | 已完成 | `notebooks/02_sklearn_regression_basics.ipynb`；`results/day2_model_metrics.csv`；`results/day2_predictions.csv`；`results/day2_model_metrics_with_binary_features.csv`；`results/day2_predictions_with_binary_features.csv`；`results/figures/day2_true_vs_predicted.png` |
| 2026-07-22 | Day 3 | 已完成 | `notebooks/03_materials_data_exploration.ipynb`；`data/raw/day3_demo_materials_database.csv`；`data/processed/day3_stable_materials.csv`；`data/processed/day3_stable_wide_gap_materials.csv`；`docs/day3_materials_data_notes.md`；Day 3 三张结果图 |

每日完成任务后，需要同步更新：

- `README.md`：记录学习计划、完成状态、产出文件和下一步。
- `AGENT.md`：记录长期目标、当前进度、协作规则和检查结果。

## 推荐项目结构

第一周可以先建立如下目录：

```text
Day03/
├── README.md
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── 01_python_pandas_basics.ipynb
│   ├── 02_materials_data_exploration.ipynb
│   └── 03_band_gap_baseline.ipynb
├── src/
└── results/
    └── figures/
```

## Day 1：明确方向，补齐 Python 数据分析基础

**状态：已完成**

**学习时长：2-4 小时**

### 今日目标

- [x] 搭好 Python 学习环境。
- [x] 熟悉 NumPy、Pandas、Matplotlib 的基本用法。
- [x] 理解“表格数据 + 机器学习”是什么形式。

### 核心任务

1. 安装或确认已有环境：已完成

   ```bash
   python --version
   pip --version
   ```

   建议安装：

   ```bash
   pip install numpy pandas matplotlib scikit-learn jupyter
   ```

2. 学习并练习 Pandas 基础：已完成

   - 读取 CSV：`pd.read_csv`
   - 查看数据：`head`、`info`、`describe`
   - 选择列：`df["band_gap"]`
   - 筛选数据：`df[df["band_gap"] > 0]`
   - 缺失值处理：`dropna`、`fillna`

3. 建立第一个 notebook：已完成

   ```text
   notebooks/01_python_pandas_basics.ipynb
   ```

### 加分任务

- 用 Matplotlib 画一个简单散点图和直方图。
- 学会设置图标题、坐标轴标签、图例。

如果使用 Python 和 Matplotlib 画图，请在创建图之前加入：

```python
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"]
plt.rcParams["mathtext.fontset"] = "stix"
```

### 今日产出

- [x] 一个能正常运行的 Jupyter Notebook：`notebooks/01_python_pandas_basics.ipynb`
- [x] 示例原始数据：`data/raw/day1_example_materials.csv`
- [x] 示例图：`results/figures/day1_band_gap_hist.png`
- [x] 示例图：`results/figures/day1_gap_vs_n_elements.png`
- [x] 处理后数据：`data/processed/wide_gap_materials.csv`
- [x] 完成 Day 1 练习检查。

### Day 1 检查记录

已完成的练习包括：

- 筛选 `band_gap_eV > 3` 的材料。
- 计算含氧材料平均带隙，结果为 `4.7425 eV`。
- 找出最大带隙材料，结果为 `Al2O3`。
- 新增 `is_wide_gap` 列。
- 保存处理后 CSV。

需要注意：

- `df["is_wide_gap"] = df["band_gap_eV"] > 3` 会生成 `True/False`；如果题目要求 `1/0`，建议使用 `(df["band_gap_eV"] > 3).astype(int)`。
- 保存宽带隙材料时，建议保存筛选后的 `wide_gap_materials`，而不是完整 `df`。

## Day 2：了解机器学习最小流程

**状态：已完成**

**学习时长：2-4 小时**

### 今日目标

- 理解监督学习、回归任务、训练集、测试集、评价指标。
- 用 Scikit-learn 跑通一个玩具回归模型。

### 核心任务

1. 学习以下概念：

   - 特征：用于预测的输入，例如组成、元素性质、结构描述符。
   - 标签：要预测的目标，例如带隙 `band_gap`。
   - 回归：预测连续数值。
   - 训练集/测试集：训练模型和评估模型的数据不能完全相同。
   - MAE：平均绝对误差，越小越好。
   - RMSE：均方根误差，对大误差更敏感。
   - R2：模型解释方差的能力，越接近 1 越好。

2. 使用 Scikit-learn 跑一个简单例子：

   - `train_test_split`
   - `LinearRegression`
   - `RandomForestRegressor`
   - `mean_absolute_error`
   - `r2_score`

3. 写下你自己的理解：

   ```text
   为什么不能只看训练集误差？
   MAE = 0.3 eV 对带隙预测意味着什么？
   ```

### 加分任务

- 对比线性回归和随机森林的结果。
- 画出 `y_true` vs `y_pred` 散点图。

### 今日产出

- [x] 一个最小回归模型 notebook：`notebooks/02_sklearn_regression_basics.ipynb`
- [x] 初始模型指标文件：`results/day2_model_metrics.csv`
- [x] 初始测试集预测结果：`results/day2_predictions.csv`
- [x] 新特征模型指标文件：`results/day2_model_metrics_with_binary_features.csv`
- [x] 新特征测试集预测结果：`results/day2_predictions_with_binary_features.csv`
- [x] 预测图：`results/figures/day2_true_vs_predicted.png`
- [x] 能解释“输入 X、目标 y、模型 model、预测 y_pred”的关系。

### Day 2 检查记录

已完成的练习包括：

- 将 `test_size` 改为 `0.4` 并重新划分训练集和测试集。
- 新增 `is_binary_compound` 特征。
- 使用 `n_elements`、`contains_oxygen`、`is_binary_compound` 三个特征重新训练线性回归和随机森林。
- 解释了小数据集上 R2 不稳定的原因。
- 分别保存了新特征模型指标和预测结果。

新特征模型结果：

```text
Linear Regression: MAE = 1.8950 eV, RMSE = 2.7891 eV, R2 = 0.2929
Random Forest:     MAE = 1.7630 eV, RMSE = 2.7958 eV, R2 = 0.2895
```

需要注意：

- 当前数据集只有 10 个样本，模型结果只适合理解流程，不能作为真实材料预测结论。
- 保存不同类型结果时要使用不同文件名，避免预测结果和指标结果互相覆盖。

## Day 3：认识材料数据库与材料机器学习问题

**状态：已完成**

**学习时长：2-4 小时**

### 今日目标

- 理解材料性质预测项目的数据来源。
- 明确第一周项目的预测目标：带隙 `band_gap`。

### 核心任务

1. 了解常见材料数据来源：

   - Materials Project
   - OQMD
   - AFLOW
   - JARVIS
   - Matbench

2. 建议第一周优先使用 Matbench 或已有 CSV 数据，而不是一开始就写 API 抓取。

   原因：第一周目标是跑通机器学习流程，不要被 API key、网络、字段格式卡住。

3. 重点了解 Matbench 中的带隙任务，例如：

   - `matbench_expt_gap`
   - `matbench_mp_gap`

4. 建立 notebook：

   ```text
   notebooks/02_materials_data_exploration.ipynb
   ```

5. 探索数据时关注：

   - 数据有多少条？
   - 目标值带隙的范围是多少？
   - 是否有金属材料，`band_gap = 0` 是否很多？
   - 是否存在缺失值？
   - 化学式字段长什么样？

### 加分任务

- 阅读一篇材料机器学习入门文章或论文摘要，重点看它如何描述特征和标签。
- 搜索关键词：`machine learning band gap prediction materials composition features`。

### 今日产出

- 一个材料数据探索 notebook：`notebooks/03_materials_data_exploration.ipynb`
- 示例材料数据库：`data/raw/day3_demo_materials_database.csv`
- 稳定材料筛选结果：`data/processed/day3_stable_materials.csv`
- 数据理解笔记：`docs/day3_materials_data_notes.md`
- 带隙分布图：`results/figures/day3_band_gap_distribution.png`
- 材料类别平均带隙图：`results/figures/day3_mean_gap_by_family.png`
- 形成能 vs 带隙散点图：`results/figures/day3_formation_energy_vs_band_gap.png`
- 宽带隙稳定材料筛选结果：`data/processed/day3_stable_wide_gap_materials.csv`

### Day 3 检查记录

已完成的练习包括：

- 筛选 `band_gap_eV > 3.0` 且 `e_above_hull_eV_atom <= 0.05` 的宽带隙稳定材料。
- 统计每个 `crystal_system` 的平均带隙。
- 绘制并保存 `formation_energy_eV_atom` vs `band_gap_eV` 散点图。
- 保存宽带隙稳定材料 CSV。
- 补完材料数据理解笔记。

关键结果：

```text
示例数据：20 个材料，7 个字段
带隙范围：0.0-8.8 eV
band_gap_eV = 0 的材料数：3
主要材料类别：oxide，共 11 个样本
宽带隙稳定材料数量：8
```

需要注意：

- 当前数据是本地示例数据，只用于学习材料数据探索流程，不能作为科研结论。
- Day 4 将开始学习如何把 `formula` 转换为数值特征。


## Day 4：学习材料特征工程

**学习时长：2-4 小时**

### 今日目标

- 理解模型不能直接“看懂”化学式，需要把材料转成数值特征。
- 掌握最基础的组成特征思路。

### 核心任务

1. 理解以下问题：

   ```text
   对机器学习模型来说，"TiO2" 不是天然可计算的数字。
   我们需要把它变成一组特征，例如平均原子序数、元素电负性统计量、元素种类数等。
   ```

2. 学习两种特征方案：

   - 简单手写特征：元素个数、是否含 O、是否含金属元素、平均原子序数等。
   - 使用现成工具：`matminer`、`pymatgen`。

3. 如果安装顺利，可以尝试：

   ```bash
   pip install pymatgen matminer
   ```

   如果安装失败，当天不要卡太久，可以先用简单手写特征完成 baseline。

4. 记录至少 5 个你认为可能影响带隙的材料特征。

### 加分任务

- 了解 `pymatgen.core.Composition` 如何解析化学式。
- 了解 `matminer.featurizers.composition` 中的组成特征。

### 今日产出

- 一个能把化学式转换成数值特征的简单函数。
- 一份特征说明，例如：

   ```text
   n_elements：元素种类数
   mean_atomic_number：按元素比例加权平均原子序数
   contains_oxygen：是否含氧
   ```

## Day 5：训练第一个材料带隙预测 baseline

**学习时长：2-4 小时**

### 今日目标

- 完成第一个真正和材料相关的机器学习模型。
- 得到 MAE、RMSE、R2 等评价结果。

### 核心任务

1. 建立 notebook：

   ```text
   notebooks/03_band_gap_baseline.ipynb
   ```

2. 完成完整流程：

   - 读取数据。
   - 清洗数据。
   - 构造特征 `X`。
   - 设置标签 `y = band_gap`。
   - 划分训练集和测试集。
   - 训练模型。
   - 评估模型。
   - 保存预测结果。

3. 至少训练两个模型：

   - `LinearRegression`
   - `RandomForestRegressor`

4. 输出评价指标：

   - MAE
   - RMSE
   - R2

### 加分任务

- 尝试 `GradientBoostingRegressor` 或 `XGBoost`。
- 画出预测值和真实值对比图。
- 画出误差分布图。

### 今日产出

- 一个可运行的带隙预测 baseline。
- 一张 `y_true` vs `y_pred` 图。
- 一张模型结果对比表。

## Day 6：整理项目，写出能投递的项目说明

**学习时长：2-4 小时**

### 今日目标

- 把 notebook 从“自己能看”整理到“别人能看懂”。
- 开始用简历语言描述项目。

### 核心任务

1. 整理 notebook 标题和小节：

   ```text
   1. 数据来源
   2. 数据探索
   3. 特征工程
   4. 模型训练
   5. 模型评估
   6. 结果分析
   ```

2. 在 `results/figures/` 保存关键图片：

   - 带隙分布图
   - 真实值 vs 预测值散点图
   - 模型误差对比图

3. 写一段项目介绍：

   ```text
   本项目基于公开材料数据集，构建组成特征并训练机器学习模型预测材料带隙。
   对比线性回归和随机森林等模型后，使用 MAE、RMSE 和 R2 评估模型性能。
   项目目标是探索传统机器学习方法在材料性质预测任务中的基本流程。
   ```

### 加分任务

- 用英文写一版项目简介。
- 把项目中的关键概念整理成面试问答。

### 今日产出

- 一个结构清晰的 notebook。
- 3 张结果图。
- 一段可放进简历的项目描述。

## Day 7：复盘、补短板、准备第二周

**学习时长：2-4 小时**

### 今日目标

- 复盘第一周内容。
- 找到最需要补的短板。
- 为第二周的深入学习做准备。

### 核心任务

1. 回答以下问题：

   ```text
   1. 这个项目的输入是什么？
   2. 输出是什么？
   3. 为什么它是回归任务？
   4. 你用了哪些特征？
   5. 哪个模型效果最好？
   6. MAE 的单位是什么？
   7. 如果 MAE = 0.5 eV，这个模型有没有实际意义？
   8. 数据集是否可能存在偏差？
   9. 如果要预测吸附能，流程需要改哪里？
   10. 这个项目如何继续提升？
   ```

2. 整理第一周学习总结：

   ```text
   docs/week1_summary.md
   ```

3. 列出第二周要提升的方向：

   - 更好的材料特征。
   - 更规范的模型评估。
   - 超参数调优。
   - 项目代码化，从 notebook 迁移到 Python 脚本。
   - 加入 README、requirements、结果图和简历描述。

### 加分任务

- 录制一个 3 分钟项目讲解，模拟面试时介绍项目。
- 用英文准备一段 self-introduction，突出“physics/materials + machine learning”交叉背景。

### 今日产出

- 第一周总结文档。
- 第二周待办清单。
- 一段 1 分钟项目口述介绍。

## 第一周最低完成标准

如果时间紧，第一周至少完成：

- 会用 Pandas 读取和查看 CSV。
- 会用 Scikit-learn 训练回归模型。
- 能解释 MAE、RMSE、R2。
- 有一个带隙预测 baseline notebook。
- 有一张真实值 vs 预测值图。
- 能用 1 分钟讲清楚项目。

## 第一周推荐学习资料

优先级从高到低：

1. Scikit-learn 官方入门教程：学习 `fit`、`predict`、`train_test_split`、评价指标。
2. Pandas 官方 10 minutes to pandas：掌握 DataFrame 基础。
3. Matplotlib 官方 quick start：掌握基础画图。
4. Matbench 或 Materials Project 相关介绍：理解材料数据集。
5. Pymatgen / Matminer 文档：了解材料特征工程。

## 简历描述草稿

第一周结束后，可以先写成这样：

```text
材料带隙机器学习预测项目：
基于公开材料数据集，使用 Python、Pandas 和 Scikit-learn 构建材料带隙预测流程；
完成数据清洗、组成特征构造、回归模型训练与误差分析；
对比线性回归和随机森林模型，并使用 MAE、RMSE、R2 评估预测性能。
```

后续第二、三周需要把这段描述升级为包含具体数据规模、模型指标和项目链接的版本。
