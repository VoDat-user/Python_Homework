# Viết chương trình đổi các từ ở đầu câu sang chữ hoa và những từ không phải đầu câu sang chữ thường.

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
def convert_text(text): 
    # Tách câu bằng dấu chấm
    sentences = text.split('.')
    result = []
    
    for sentence in sentences:
        if sentence.strip():  # Kiểm tra câu không rỗng
            # Tách từ trong câu
            words = sentence.strip().split()
            if words:
                # Chuyển từ đầu tiên thành chữ hoa, các từ còn lại thành chữ thường
                words[0] = words[0].capitalize()
                for i in range(1, len(words)):
                    words[i] = words[i].lower()
                result.append(' '.join(words))
    
    return '. '.join(result) + '.'

# Test thử chương trình
test_text = "hello WORLD. HOW are YOU today. python IS awesome"
print("Văn bản gốc:", test_text)
print("Sau khi chuyển đổi:", convert_text(test_text))