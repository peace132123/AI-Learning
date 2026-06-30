import pandas as pd
import os
from datetime import datetime

class ExamScoreManager:
    def __init__(self, filename='exam_scores.xlsx'):
        """初始化成绩管理器"""
        self.filename = filename
        self.columns = ['考试名称', '语文', '数学', '英语', '物理', '化学', '政治']
        self.existing_df = None
        self.load_existing_data()

    def load_existing_data(self):
        """加载已有的数据"""
        if os.path.exists(self.filename):
            try:
                self.existing_df = pd.read_excel(self.filename)
                print(f"✅ 已加载已有数据，共 {len(self.existing_df)} 次考试记录\n") # len(self.existing_df)输出表格行数
            except Exception as e:
                print(f"⚠️ 读取文件出错：{e}")
                self.existing_df = None
    
    def input_exan_data(self):
        """输入考试数据"""
        print("=" * 55)
        print("📝 录入考试成绩")
        print("=" * 55)

        # 输入考试名称
        exam_name = input("请输入考试名称（如：期中考试、月考1等）：").strip() # 去除输入时首位的空格字符
        if not exam_name:
            exam_name = f"考试_{datetime.now().strftime('%m%d_%H%M')}" #生成一个带有当前日期和时间的考试名称字符串
            print(f" 使用默认名称：{exam_name}")

        scores = {}
        subjects = ['语文', '数学', '英语', '物理', '化学', '政治']

        print("\n 请输入各科成绩")
        print("-" * 35)

        for subject in subjects:
            while True:
                try:
                    score = float(input(input(f" {subject}:")))
                    if 0 <= score <= 150:
                        scores[subject] = score
                        break
                    else:
                        print("  ❌ 成绩应在0-150之间")
                except ValueError:
                    print("  ❌ 请输入有效数字")
        
        return exam_name, scores
    
    def compare_with_previos(self, exam_name, current_scores):
        """与上次考试相比"""
        if self.existing_df is None or len(self.existing_df) == 0:
            print("\n" + "=" * 65)
            print(f"📊 第1次考试记录")
            print("=" * 65)
            print(f"\n📋 考试名称：{exam_name}")
            print("-" * 75)
            print(f"{'科目':<8}{'本次成绩':<10}")
            print("-" * 20)
            for subject, score in current_scores.items():
                print(f"{subject:<8}{score:<10.1f}")
            print("-" * 22)
            print("ℹ️  这是第一次考试，无历史数据可对比")
            return

        # 获取上次考试数据
        last_row = self.existing_df.iloc[-1]
        last_exam_name = last_row['考试名称']

        print("\n" + "=" * 95)
        print(f"📊 成绩对比分析")
        print("=" * 95)
        print(f"\n📋 当前考试：{exam_name}")
        print(f"📋 上次考试：{last_exam_name}")
        print("-" * 110)
        print(f"{'科目':<8}{'本次成绩':<10}{'上次成绩':<10}{'进步/退步':<15}{'变化趋势'}")
        print("-" * 115)   
    
        total_progress = 0
        progress_count = 0
        regress_count = 0

        for subject in self.columns[1:]:
            current = current_scores[subject]
            previous = last_row[subject]
            diff = current - previous

            if diff > 0:
                trend = "↑ 进步"
                symbol = "📈"
                progress_count += 1
            elif diff <0 :
                trend = "↓ 退步"
                symbol = "📉"
                regress_count += 1
            else:
                trend = "→ 持平"
                symbol = "➡️"
            
            diff_str = f"+{diff:.1f}" if diff > 0 else f"{diff:.1f}" if diff < 0 else "0.0"
            print(f"{subject:<8}{current:<10.1f}{previous:10.1f}{diff_str:<15}{symbol}{trend}")
            total_progress += diff
        
        print("-" * 105)

        #总体评价
        avg_diff = total_progress / 6
        print(f"\n📊 总体分析：")
        print(f"   📈 进步科目：{progress_count} 科")
        print(f"   📉 退步科目：{regress_count} 科")
        print(f"   ➡️ 持平科目：{6 - progress_count - regress_count} 科")
        print(f"   📊 总分变化：{total_progress:+.1f} 分")
        print(f"   📊 平均变化：{avg_diff:+.1f} 分")

        if avg_diff > 5:
            print(f"\n   🎉 总体表现优秀，继续保持！")
        elif avg_diff > 0:
            print(f"\n   👍 略有进步，再接再厉！")
        elif avg_diff > -5:
            print(f"\n   🤔 略有退步，需要加油！")
        else:
            print(f"\n   💪 退步较大，要更加努力了！")
        
        print("\n" + "=" * 97)

    def save_to_excel(self, exam_name, scores):
        """保存到Excel文件"""
        #创建新的数据行
        new_row = {"考试名称": exam_name}
        for subject, score in scores.items():
            new_row[subject] = score

        new_df = pd.DataFrame([new_row])

        # 合并数据
        if self.existing_df is not None and len(self.existing_df) > 0:
            combined_df = pd.contcat([self.existing_df, new_df], ignore_index=True)
        else:
            combined_df = new_df

        # 保存到Excel
        try:
            combined_df.to_excel(self.filename, index=False)
            print(f"\n✅ 数据已保存到 {self.filename}")
            print(f"📊 当前共有 {len(combined_df)} 次考试记录")
        except Exception as e:
            print(f"❌ 保存失败：{e}")

    def run(self):
        """运行主流程"""
        print("\n" + "=" * 52)
        print("🎯 学生考试成绩管理系统")
        print("=" * 53)

        # 输入考试数据
        exam_name, scores = self.input_exam_data()

        # 与上次考试相比
        self.compare_with_previos(exam_name, scores)

        # 保存数据
        self.save_to_excel(exam_name, scores)

        # 询问是否继续
        while True:
            print("\n" + "-" * 42)
            choice = input("是否继续录入下次考试？(y/n):").strip().lower()
            if choice == 'y':
                self.run()
                break
            elif choice == 'n':
                print("\n 👋 感谢使用，再见！")
                break
            else:
                print("❌ 请输入 y 或 n")

# 查看历史成绩功能
def view_history(filename='exam_scores.xlsx'):
    """查看历史成绩"""
    if not os.path.exists(filename):
        print("⚠️ 没有找到成绩文件")
        return
    
    try:
        df = pd.read_excel(filename)
        if len(df) == 0:
            printt("⚠️ 成绩文件为空")
            return
        
        print("\n" + "=" * 70)
        print("📚 历史成绩总览")
        print("=" * 72)
        print(df.to_string(index=False))
        print("=" * 73)
        
        # 显示各科平均分
        print("\n📊 各科平均分：")
        for col in df.columns[1:]:
            avg = df[col].mean()
            print(f" {col}:{avg:.2f} 分")

        # 显示最高分记录
        print("\n🏆 各科最高分：")
        for col in df.columns[1:]:
            max_val = df[col].max()
            best_exam = df.loc[df[col].idxmax(), '考试名称']
            print(f" {col}:{max_val:.1f}分({best_exam})")

    except Exception as e:
        print(f"❌ 读取失败：{e}")


# 导出为csv功能
def export_to_csv(filename='exam_scores.xlsx', csv_filename='exam_scores.csv'):
    """导出为csv格式"""
    if not os.path.exists(filename):
        print("⚠️ 没有找到成绩文件")
        return
    
    try:
        df = pd.read_excel(filename)
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
        print(f"✅ 已导出到 {csv_filename}")
    except Exception as e:
        print(f"❌ 导出失败：{e}")


def main():
    """主菜单"""
    while True:
        print("\n" + "=" * 48)
        print("🎯 学生考试成绩管理系统")
        print("=" * 49)
        print("1. 📝 录入新考试成绩")
        print("2. 📊 查看历史成绩")
        print("3. 📁 导出为CSV文件")
        print("4. 🚪 退出系统")
        print("=" * 51)

        choice = input("请选择操作（1-4）：").strip()

        if choice == '1':
            manager = ExamScoreManager()
            manager.run()

        elif choice == '2':
            view_history()

        elif choice == '3':
            export_to_csv()

        elif choice == '4':
            print("\n👋 感谢使用，再见！")
            break

        else:
            print("❌ 无效选择，请重新输入")

    
if __name__ == '__main__':
    main()
    