# Dao nguoc tu
def dao_nguoc_tu(chuoi):
  words = chuoi.split()
  words.reverse()
  return ' '.join(words)

# Run CodeCode
chuoi_ban_dau = "Không Thầy đố mày làm nên"
chuoi_da_dao_nguoc = dao_nguoc_tu(chuoi_ban_dau)
print(f"Chuỗi ban đầu: {chuoi_ban_dau}")
print(f"Chuỗi đã đảo ngược: {chuoi_da_dao_nguoc}")