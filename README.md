# Nền Tảng Quản Lý Tình Nguyện Viên

## Giới Thiệu Chung

Dự án này là một ứng dụng web được xây dựng bằng Django, nhằm mục đích quản lý các sự kiện tình nguyện. Nền tảng cho phép người dùng đăng ký tài khoản, duyệt, tìm kiếm và đăng ký tham gia các sự kiện. Quản trị viên và người tổ chức sự kiện có thể quản lý (thêm, sửa, xóa) các sự kiện, tạo báo cáo sau sự kiện và xem các thống kê trực quan về hoạt động của nền tảng.

Ứng dụng được thiết kế với giao diện thân thiện, dễ sử dụng, tập trung vào việc kết nối tình nguyện viên với các cơ hội đóng góp cho cộng đồng và giúp các tổ chức quản lý hiệu quả các hoạt động tình nguyện của mình.

## Cấu Trúc Dự Án

```
volunteer_project/
├── .git/
├── db.sqlite3
├── media/
│   ├── event_covers/
│   └── event_reports/
├── staticfiles/  (Collected static files for production)
├── volunteer/    (Main application)
│   ├── migrations/
│   ├── static/
│   │   └── volunteer/
│   │       ├── css/
│   │       ├── image/ (Charts are saved here)
│   │       └── js/
│   ├── templates/
│   │   └── volunteer/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── volunteer_project/ (Project configuration)
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── README.md
└── requirements.txt
```

## Tính Năng Chính

### Dành cho Người Dùng (Tình Nguyện Viên)

1.  **Xác thực Người Dùng**:

    - Đăng ký tài khoản mới.
    - Đăng nhập vào hệ thống.
    - Đăng xuất khỏi tài khoản.

2.  **Quản Lý Hồ Sơ Cá Nhân**:

    - Xem thông tin cá nhân: tuổi, số điện thoại, địa chỉ, kỹ năng.
    - Cập nhật thông tin cá nhân.
    - Xem tổng số giờ tình nguyện đã tích lũy.

3.  **Khám Phá và Tham Gia Sự Kiện**:

    - **Trang chủ**: Hiển thị danh sách các sự kiện nổi bật hoặc mới nhất.
    - **Trang Hoạt động (Dashboard)**: Hiển thị danh sách các sự kiện, có thể lọc theo các tiêu chí như:
      - Tất cả sự kiện.
      - Sự kiện đã tham gia.
      - Sự kiện chưa tham gia.
      - Sự kiện đã yêu thích.
      - Sự kiện được gợi ý dựa trên kỹ năng (nếu người dùng đã cung cấp).
      - Sự kiện do người dùng tổ chức.
    - **Tìm kiếm và Lọc Sự Kiện**:
      - Tìm kiếm sự kiện theo tên, mô tả, địa điểm.
      - Lọc sự kiện theo danh mục (ví dụ: Giáo dục, Môi trường, Y tế) và trạng thái (ví dụ: Sắp diễn ra, Đang diễn ra, Đã kết thúc).
    - **Xem Chi Tiết Sự Kiện**:
      - Thông tin đầy đủ về sự kiện: tên, thời gian bắt đầu/kết thúc, địa điểm, mô tả chi tiết, số giờ tình nguyện, số lượng người tham gia tối đa/hiện tại.
      - Thông tin người tổ chức.
      - Ảnh bìa sự kiện.
    - **Tương Tác với Sự Kiện**:
      - **Đăng ký tham gia**: Nếu sự kiện còn chỗ và người dùng chưa đăng ký.
      - **Hủy đăng ký tham gia**.
      - **Yêu thích/Bỏ yêu thích** sự kiện.
      - **Chia sẻ** sự kiện (hệ thống ghi nhận số lượt chia sẻ).
    - **Xem danh sách sự kiện đã tham gia và đã tổ chức** trên trang hồ sơ.

4.  **Trang Quyên Góp**: Một trang tĩnh cung cấp thông tin về việc quyên góp (nếu có).

### Dành cho Quản Trị Viên (Admin) và Người Tổ Chức Sự Kiện

1.  **Quản Lý Sự Kiện**:

    - **Tạo sự kiện mới**: Cung cấp đầy đủ thông tin như tên, mô tả, thời gian, địa điểm, danh mục, số giờ tình nguyện, số lượng người tham gia tối đa, ảnh bìa.
    - **Cập nhật thông tin sự kiện** hiện có.
    - **Xóa sự kiện**.
    - _(Chỉ Admin hoặc người tổ chức sự kiện đó mới có quyền sửa/xóa)_.

2.  **Báo Cáo Sự Kiện**:

    - **Tạo báo cáo** cho các sự kiện đã hoàn thành: tiêu đề báo cáo, số người tham gia thực tế, nội dung chi tiết, kết quả đạt được, thách thức gặp phải, và tải lên nhiều hình ảnh minh họa cho báo cáo.
    - **Cập nhật báo cáo** đã tạo.
    - **Xem báo cáo chi tiết** của sự kiện.
    - _(Chỉ Admin hoặc người tổ chức sự kiện đó mới có quyền tạo/sửa báo cáo)_.

3.  **Thống Kê (Dành cho Admin)**:

    - Truy cập trang thống kê để xem các biểu đồ trực quan:
      - **Biểu đồ cột**: Phân loại số lượng sự kiện theo trạng thái (Đang lên kế hoạch, Đang diễn ra, Đã kết thúc).
      - **Biểu đồ đường**: Thống kê số lượng sự kiện được tạo theo từng tháng trong năm hiện tại.
    - Các biểu đồ này được tự động tạo và lưu dưới dạng hình ảnh trong thư mục `volunteer/static/volunteer/image/`.

4.  **Quản lý Người Dùng (thông qua Django Admin Interface)**:
    - Xem danh sách người dùng.
    - Chỉnh sửa thông tin người dùng.
    - Gán quyền quản trị.

## Các Mô Hình Cơ Sở Dữ Liệu Chính

### `CustomUser` (Mở rộng từ `AbstractUser` của Django)

- `age` (Tuổi): Kiểu PositiveIntegerField (số nguyên dương).
- `phone_number` (Số điện thoại): Kiểu CharField.
- `address` (Địa chỉ): Kiểu TextField.
- `skills` (Kỹ năng): Kiểu TextField (lưu trữ các kỹ năng, có thể cách nhau bằng dấu phẩy).
- `volunteer_hours` (Số giờ tình nguyện): Kiểu PositiveIntegerField, mặc định là 0.
- `is_admin` (Là quản trị viên): Kiểu BooleanField, mặc định là False.

### `Event` (Sự kiện)

- `name` (Tên sự kiện): Kiểu CharField.
- `start_time` (Thời gian bắt đầu): Kiểu DateTimeField.
- `end_time` (Thời gian kết thúc): Kiểu DateTimeField.
- `location` (Địa điểm): Kiểu CharField.
- `description` (Mô tả): Kiểu TextField.
- `volunteer_hours` (Số giờ tình nguyện cho sự kiện): Kiểu PositiveIntegerField.
- `max_participants` (Số người tham gia tối đa): Kiểu PositiveIntegerField (0 nghĩa là không giới hạn).
- `cover_image` (Ảnh bìa): Kiểu ImageField, tải lên thư mục `media/event_covers/`.
- `category` (Danh mục): Kiểu CharField, với các lựa chọn được định nghĩa trước (Giáo dục, Môi trường, Y tế, Cộng đồng, Khác).
- `status` (Trạng thái): Kiểu CharField, với các lựa chọn được định nghĩa trước (Đang lên kế hoạch, Đang diễn ra, Đã kết thúc).
- `organizer` (Người tổ chức): Khóa ngoại (ForeignKey) đến `CustomUser`.
- `participants` (Người tham gia): Quan hệ Nhiều-Nhiều (ManyToManyField) đến `CustomUser`, thông qua mô hình trung gian `EventParticipation`.
- `viewers` (Người xem): Quan hệ Nhiều-Nhiều đến `CustomUser` (theo dõi lượt xem).
- `likes` (Lượt thích): Quan hệ Nhiều-Nhiều đến `CustomUser`.
- `shares` (Lượt chia sẻ): Kiểu PositiveIntegerField, mặc định là 0.
- `created_at` (Thời điểm tạo): Kiểu DateTimeField, tự động thêm khi tạo.
- `updated_at` (Thời điểm cập nhật): Kiểu DateTimeField, tự động cập nhật khi có thay đổi.

### `EventParticipation` (Tham gia sự kiện)

- `user` (Người dùng): Khóa ngoại đến `CustomUser`.
- `event` (Sự kiện): Khóa ngoại đến `Event`.
- `registered_at` (Thời điểm đăng ký): Kiểu DateTimeField, tự động thêm khi tạo.
- `attended` (Đã tham dự): Kiểu BooleanField, mặc định là False (có thể dùng để điểm danh).
- _Meta_: `unique_together = ['user', 'event']` (Đảm bảo mỗi người dùng chỉ đăng ký một sự kiện một lần).

### `EventReport` (Báo cáo sự kiện)

- `event` (Sự kiện): Quan hệ Một-Một (OneToOneField) đến `Event`.
- `title` (Tiêu đề báo cáo): Kiểu CharField.
- `actual_participants` (Số người tham gia thực tế): Kiểu PositiveIntegerField.
- `report_content` (Nội dung báo cáo): Kiểu TextField.
- `achievements` (Kết quả đạt được): Kiểu TextField.
- `challenges` (Thách thức gặp phải): Kiểu TextField.
- `images` (Hình ảnh báo cáo chính): Kiểu ImageField, tải lên `media/event_reports/`. (Lưu ý: Mô hình `ReportImage` dùng để lưu nhiều ảnh).
- `report_date` (Ngày báo cáo): Kiểu DateTimeField, tự động thêm khi tạo.
- `created_by` (Người tạo báo cáo): Khóa ngoại đến `CustomUser`.

### `ReportImage` (Hình ảnh báo cáo)

- `report` (Báo cáo): Khóa ngoại đến `EventReport` (quan hệ ngược `report_images`).
- `image` (Hình ảnh): Kiểu ImageField, tải lên `media/event_reports/`.
- `uploaded_at` (Thời điểm tải lên): Kiểu DateTimeField, tự động thêm khi tạo.

## Hướng Dẫn Cài Đặt và Sử Dụng

### Chuẩn Bị Môi Trường

1.  **Clone dự án từ repository:**

    ```bash
    git clone https://github.com/NghiaAi/volunteer-management-system.git
    cd volunteer_project
    ```

2.  **Tạo và kích hoạt môi trường ảo (khuyến nghị):**
    Việc này giúp cô lập các thư viện của dự án, tránh xung đột với các dự án khác.

    ```bash
    # Lệnh cho Windows
    python -m venv venv
    venv\Scripts\activate

    # Lệnh cho macOS/Linux
    python3 -m venv venv  # Hoặc python -m venv venv
    source venv/bin/activate
    ```

3.  **Cài đặt các thư viện cần thiết:**
    Các thư viện được liệt kê trong tệp `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```
    Danh sách các thư viện chính:
    - `Django==5.0.7`: Framework chính của dự án.
    - `Pillow==10.1.0`: Thư viện xử lý hình ảnh.
    - `django-crispy-forms==2.1`: Giúp quản lý và hiển thị form đẹp hơn.
    - `crispy-bootstrap5==0.7`: Gói template Bootstrap 5 cho `django-crispy-forms`.
    - `matplotlib==3.10.0`: Thư viện trực quan
    - `seaborn==0.13.2`: Thư viện trực quan

### Cấu Hình Cơ Sở Dữ Liệu và Chạy Ứng Dụng

4.  **Áp dụng các di trú (migrations) để tạo bảng trong cơ sở dữ liệu:**
    Lệnh này sẽ tạo các bảng dựa trên định nghĩa trong `models.py`.

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Tạo tài khoản superuser (quản trị viên cấp cao nhất):**
    Tài khoản này dùng để truy cập vào giao diện quản trị của Django (`/admin/`).

    ```bash
    python manage.py createsuperuser
    ```

    Bạn sẽ được yêu cầu nhập tên người dùng, địa chỉ email (tùy chọn) và mật khẩu.

6.  **Chạy máy chủ phát triển (development server):**
    ```bash
    python manage.py runserver
    ```
    Ứng dụng sẽ chạy và có thể truy cập tại địa chỉ `http://127.0.0.1:8000/` trên trình duyệt của bạn.

### Hướng Dẫn Sử Dụng Cơ Bản

1.  **Đăng ký/Đăng nhập**:

    - Truy cập trang chủ, nhấp vào nút "Đăng ký" để tạo tài khoản mới hoặc "Đăng nhập" nếu đã có tài khoản.
    - Điền đầy đủ thông tin theo biểu mẫu.

2.  **Người dùng (Tình nguyện viên)**:

    - **Xem sự kiện**: Duyệt các sự kiện trên trang chủ hoặc trang "Hoạt Động". Sử dụng bộ lọc và thanh tìm kiếm để tìm sự kiện phù hợp.
    - **Xem chi tiết**: Nhấp vào một sự kiện để xem thông tin chi tiết.
    - **Tương tác**:
      - Nhấp "Tham gia" để đăng ký (nếu đủ điều kiện).
      - Nhấp "Yêu thích" (biểu tượng trái tim).
    - **Quản lý hồ sơ**: Truy cập trang "Hồ sơ" từ menu người dùng để xem/chỉnh sửa thông tin cá nhân và xem các sự kiện đã tham gia/tổ chức.

3.  **Người tổ chức/Quản trị viên**:
    - **Tạo sự kiện**: Từ trang "Hoạt Động" (nếu có quyền), nhấp nút "Tạo Sự Kiện Mới". Điền thông tin và lưu lại.
    - **Chỉnh sửa/Xóa sự kiện**: Trong trang chi tiết sự kiện mà bạn quản lý, sẽ có các nút "Chỉnh sửa" hoặc "Xóa".
    - **Tạo báo cáo**: Sau khi sự kiện có trạng thái "Đã kết thúc", người tổ chức/admin có thể vào chi tiết sự kiện và tìm tùy chọn để "Tạo báo cáo sự kiện".
    - **Xem thống kê**: Nếu là Admin, truy cập mục "Thống kê" từ menu chính để xem các biểu đồ.
    - **Quản trị nâng cao**: Truy cập `/admin/` bằng tài khoản superuser để quản lý toàn bộ dữ liệu hệ thống (người dùng, sự kiện, báo cáo, v.v.).
