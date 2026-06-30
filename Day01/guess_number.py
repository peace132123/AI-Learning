import random


def play_game() -> None:
    target = random.randint(1, 500)
    attempts = 0

    print("\n我已经想好了一个 1～500 之间的整数，你有 3 次机会。")

    while attempts < 3:
        user_input = input("请输入你猜的数字（输入 q 退出）：").strip()

        if user_input.lower() == "q":
            print(f"游戏已退出，正确答案是 {target}。")
            return

        try:
            guess = int(user_input)
        except ValueError:
            print("请输入有效的整数。")
            continue

        if not 1 <= guess <= 500:
            print("数字必须在 1～500 之间。")
            continue

        attempts += 1

        if guess < target:
            print(f"猜小了，还剩 {3 - attempts} 次机会。")
        elif guess > target:
            print(f"猜大了，还剩 {3 - attempts} 次机会。")
        else:
            print(f"恭喜你猜对了！你一共猜了 {attempts} 次。")
            return

    print(f"三次机会已经用完，正确答案是 {target}。")


def main() -> None:
    print("欢迎来到猜数字小游戏！")

    while True:
        play_game()
        choice = input("\n是否再玩一局？（y/n）：").strip().lower()
        if choice not in {"y", "yes", "是"}:
            print("感谢游玩，再见！")
            break


if __name__ == "__main__":
    main()
