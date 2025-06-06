import random
import time

def generate_random_number():
    """Tạo số ngẫu nhiên từ miligiây của thời gian hiện tại"""
    current_time = int(time.time() * 1000)
    return (current_time % 999) + 1

def get_player_guess():
    """Nhận và kiểm tra số đoán từ người chơi"""
    while True:
        guess = input("\nNhập số đoán của bạn (1-999) hoặc 'Stop' để dừng trò chơi: ")
        
        if guess.lower() == 'stop':
            return 'stop'
        
        try:
            guess = int(guess)
            if 1 <= guess <= 999:
                return guess
            print("Vui lòng nhập số từ 1 đến 999!")
        except ValueError:
            print("Vui lòng nhập một số nguyên!")

def check_guess(guess, target):
    """Kiểm tra và đưa ra gợi ý cho số đoán"""
    if guess == target:
        return "correct"
    elif abs(guess - target) <= 10:
        return "close"
    elif guess < target:
        return "low"
    else:
        return "high"

def play_game():
    """Hàm chính của trò chơi"""
    target = generate_random_number()
    wrong_guesses = 0
    
    while True:
        # Debug line - remove in production
        # print(f"Số cần tìm là: {target}")
        
        guess = get_player_guess()
        if guess == 'stop':
            print("\nCảm ơn bạn đã chơi! Tạm biệt!")
            return
            
        result = check_guess(guess, target)
        
        if result == "correct":
            print(f"\nChúc mừng! Bạn đã đoán đúng số {target}!")
            return
            
        wrong_guesses += 1
        print(f"Bạn đã trả lời sai {wrong_guesses} lần")
        
        if wrong_guesses == 5:
            print("\nBạn đoán trật tất cả năm lần, kết quả đã thay đổi. Mời bạn đoán lại")
            target = generate_random_number()
            wrong_guesses = 0
            continue
            
        # Đưa ra gợi ý
        if result == "close":
            print("Bạn đoán gần đúng rồi!")
        elif result == "low":
            print("Số của bạn nhỏ hơn số cần tìm")
        else:
            print("Số của bạn lớn hơn số cần tìm")

if __name__ == "__main__":
    print("\nChào mừng đến với trò chơi Đoán Số!")
    print("Hãy đoán một số từ 1 đến 999")
    print("Để dừng trò chơi, nhập: Stop!")
    print("-" * 50)
    play_game()