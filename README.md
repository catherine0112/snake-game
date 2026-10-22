# 🐍 Ultimate Snake Game

Trò chơi Rắn săn mồi được viết bằng **Python** và **Pygame**, với 3 chế độ chơi, tường di chuyển, vật phẩm đặc biệt và nhạc nền thay đổi theo level.



## ✨ Tính năng

- **Nhập tên người chơi** và menu chọn độ khó có nhạc nền riêng
- **3 chế độ chơi** với độ khó tăng dần (xem bảng bên dưới)
- **Hệ thống level**: cứ mỗi 10 điểm lên 1 level, tốc độ tăng, màu nền đổi, nhạc nền đổi ngẫu nhiên
- **Tường di chuyển** từ level 2 (chế độ Tactician và Legend), tốc độ di chuyển nhanh dần theo level
- **Tường tàng hình** ở chế độ Legend: chỉ hiện ra khi rắn lại gần trong phạm vi 4 ô
- **Vật phẩm đặc biệt** ở chế độ Legend (xem bên dưới)
- Đồ họa rắn tự thiết kế (đầu, thân, đuôi, góc cua) và hiệu ứng âm thanh đầy đủ
- Tự động chuyển sang chế độ vẽ hình khối đơn giản nếu thiếu file đồ họa

## 🎮 Các chế độ chơi

| Phím | Chế độ | Tốc độ ban đầu | Đặc điểm |
|------|--------|----------------|----------|
| `1` | Classic | 9 | Không có chướng ngại vật |
| `2` | Tactician | 11 | Có tường, tường di chuyển từ level 2 |
| `3` | Legend | 12 | Bản đồ lưới nhỏ hơn (ô 20px), nhiều tường, tường tàng hình, vật phẩm ma thuật |

## 🧪 Vật phẩm (chế độ Legend)

| Vật phẩm | Hiệu ứng |
|----------|----------|
| 🍎 Táo đỏ | +1 điểm, rắn dài thêm 1 đoạn |
| 🍏 Táo tím/xanh (độc) | Giảm tốc độ đi 2 |
| ⚪ Orb | **Ghost Mode** 10 giây: xuyên tường, xuyên thân, đi qua mép màn hình sang phía đối diện |
| 🟣 Cổng dịch chuyển | Dịch chuyển rắn đến vị trí của thức ăn |
| 🔶 Kim cương | **Breaker Mode** 10 giây: đâm vào tường sẽ phá hủy cả cụm tường |

## ⌨️ Điều khiển

| Phím | Chức năng |
|------|-----------|
| `↑` `↓` `←` `→` | Điều khiển rắn |
| `1` `2` `3` | Chọn chế độ ở menu |
| `Enter` | Xác nhận tên người chơi |
| `C` | Chơi lại (khi Game Over) |
| `M` | Về menu (khi Game Over) |
| `Q` | Thoát game (khi Game Over) |

## 🚀 Cài đặt và chạy

**Yêu cầu:** Python 3.8-3.13.

```bash
# 1. Tải project về
git clone https://github.com/catherine0112/snake-game.git
cd snake-game

# 2. Cài Pygame
pip install pygame

# 3. Chạy game
python snake.py
```

## 📁 Cấu trúc thư mục

```
snake-game/
├── snake.py               # Code chính của game
├── snakebackground.jpg    # Ảnh nền menu
├── Graphics/              # Hình ảnh rắn và táo (head_*, body_*, tail_*, apple)
├── Sound/                 # Nhạc nền và hiệu ứng âm thanh
└── README.md
```

## 🛠️ Công nghệ

- Python 3
- Pygame

## 📝 Ghi chú

- Cửa sổ game có kích thước 1300×720 (khu vực chơi 1000×720 và bảng thông tin bên phải).
- Nếu thiếu file âm thanh, game vẫn chạy bình thường nhưng sẽ không có tiếng.

## 🙏 Credits

- Code và thiết kế game: **catherine0112**



