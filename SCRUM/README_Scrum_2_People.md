# File Excel Quản Lý Scrum cho Team 2 Người - Dự Án Volunteer Management System

## Tổng Quan

File `Volunteer_Management_Scrum_2_People.xlsx` được thiết kế đặc biệt cho team phát triển 2 người, tối ưu hóa quy trình Scrum cho dự án **Hệ Thống Quản Lý Tình Nguyện Viên**. File này bao gồm tất cả các thành phần cần thiết để quản lý dự án theo phương pháp Agile/Scrum một cách hiệu quả.

## Cấu Trúc File Excel

### 📋 1. Product Backlog

**Mục đích**: Quản lý tất cả User Stories của dự án

**Các cột chính**:

- **ID**: Mã định danh User Story (US001, US002, ...)
- **User Story**: Mô tả tính năng theo format "Là [ai], tôi muốn [gì], để [mục đích]"
- **Acceptance Criteria**: Tiêu chí chấp nhận chi tiết
- **Priority**: Độ ưu tiên (High/Medium/Low)
- **Story Points**: Ước tính độ phức tạp (Fibonacci: 1,2,3,5,8,13,21)
- **Sprint**: Sprint được assign
- **Status**: Trạng thái (Not Started/In Progress/Completed/Blocked)
- **Assignee**: Người được giao (Developer 1/Developer 2)
- **Notes**: Ghi chú bổ sung

**Màu sắc trạng thái**:

- 🟢 **Xanh lá**: Completed
- 🟡 **Vàng**: In Progress
- 🔴 **Đỏ**: Not Started
- 🟠 **Cam**: Blocked

### 🎯 2. Sprint Planning

**Mục đích**: Lập kế hoạch chi tiết cho từng Sprint

**Thông tin bao gồm**:

- **Sprint Goal**: Mục tiêu chính của Sprint
- **Duration**: Thời gian (2 tuần/Sprint)
- **User Stories**: Danh sách US trong Sprint
- **Total Story Points**: Tổng điểm Story Points
- **Team Capacity**: Khả năng làm việc của team (80 giờ/Sprint cho 2 người)
- **Status**: Trạng thái Sprint

**Kế hoạch 6 Sprints**:

1. **Sprint 1**: Authentication & User Management (13 points)
2. **Sprint 2**: Core Event Management (26 points)
3. **Sprint 3**: Event Participation System (8 points)
4. **Sprint 4**: Reporting & Analytics (16 points)
5. **Sprint 5**: Social Features (8 points)
6. **Sprint 6**: Advanced Features (21 points)

### 📅 3. Daily Scrum Template

**Mục đích**: Template cho daily standup meetings

**Cấu trúc 3 câu hỏi chuẩn**:

- **What I did yesterday**: Công việc đã hoàn thành
- **What I will do today**: Kế hoạch hôm nay
- **Blockers/Issues**: Vướng mắc cần hỗ trợ

**Cách sử dụng**:

- Cập nhật hàng ngày cho cả 2 team members
- Ghi rõ ngày tháng
- Highlight các blockers để giải quyết nhanh

### 👥 4. Team Capacity Planning

**Mục đích**: Quản lý workload và capacity của team

**Metrics theo dõi**:

- **Available Hours**: Giờ có thể làm việc
- **Committed Hours**: Giờ cam kết trong Sprint
- **Actual Hours**: Giờ thực tế đã làm
- **Utilization %**: Tỷ lệ sử dụng capacity
- **Notes**: Ghi chú về performance

**Lợi ích**:

- Theo dõi hiệu suất team
- Cải thiện estimation cho Sprint sau
- Cân bằng workload giữa 2 developers

### ⚠️ 5. Risk Management

**Mục đích**: Quản lý rủi ro dự án

**Thông tin rủi ro**:

- **Risk ID**: Mã định danh rủi ro
- **Description**: Mô tả chi tiết rủi ro
- **Probability**: Xác suất xảy ra (Low/Medium/High)
- **Impact**: Mức độ tác động (Low/Medium/High)
- **Risk Level**: Mức độ rủi ro tổng thể
- **Mitigation Strategy**: Chiến lược giảm thiểu
- **Owner**: Người chịu trách nhiệm
- **Status**: Trạng thái (Active/Mitigated/Monitoring)

**Rủi ro chính đã xác định**:

- Team member nghỉ ốm
- Requirements thay đổi
- Technical debt tích lũy
- Database performance issues
- Deployment issues

### ✅ 6. Definition of Done

**Mục đích**: Tiêu chí hoàn thành cho mọi task

**Các danh mục**:

- **Code Quality**: Review, standards, no errors
- **Testing**: Unit tests, manual testing, cross-browser
- **Documentation**: Comments, README updates
- **Deployment**: Staging deployment, migrations
- **User Experience**: Responsive, accessibility
- **Security**: Input validation, authentication
- **Performance**: Load time < 3 seconds
- **Integration**: API functionality

### 📊 7. Burndown Chart Data

**Mục đích**: Dữ liệu để tạo burndown charts

**Thông tin theo dõi**:

- **Remaining Story Points**: Điểm còn lại theo ngày
- **Ideal Burndown**: Đường lý tưởng
- **Actual Burndown**: Tiến độ thực tế

### 🔄 8. Sprint Retrospective

**Mục đích**: Cải tiến liên tục sau mỗi Sprint

**Cấu trúc**:

- **What Went Well**: Điều tốt cần duy trì
- **What Could Be Improved**: Điều cần cải thiện
- **Action Items**: Hành động cụ thể
- **Owner**: Người chịu trách nhiệm
- **Due Date**: Hạn hoàn thành

## Hướng Dẫn Sử Dụng cho Team 2 Người

### 🎭 Phân Chia Vai Trò

**Developer 1** (có thể kiêm Scrum Master):

- Quản lý Product Backlog
- Facilitate Daily Scrum
- Update Sprint progress
- Risk management
- Retrospective facilitation

**Developer 2** (có thể kiêm Product Owner):

- Prioritize User Stories
- Define Acceptance Criteria
- Sprint goal definition
- Stakeholder communication
- Quality assurance

### 📅 Quy Trình Hàng Ngày

**Daily Standup (15 phút)**:

1. Mở sheet "Daily Scrum Template"
2. Cập nhật 3 câu hỏi cho cả 2 người
3. Discuss blockers và support
4. Update task status trong "Product Backlog"

**Weekly Review**:

1. Review "Team Capacity Planning"
2. Update "Risk Management"
3. Adjust Sprint plan nếu cần

### 🔄 Quy Trình Sprint

**Sprint Planning (2 giờ)**:

1. Review "Product Backlog"
2. Select User Stories cho Sprint mới
3. Update "Sprint Planning" sheet
4. Estimate capacity trong "Team Capacity Planning"

**Sprint Review & Retrospective (1.5 giờ)**:

1. Demo completed features
2. Update "Sprint Retrospective"
3. Plan action items
4. Update capacity data

### 📈 Metrics và KPIs

**Velocity Tracking**:

- Story points completed per sprint
- Team utilization percentage
- Burndown rate

**Quality Metrics**:

- Definition of Done compliance
- Number of bugs per sprint
- Code review coverage

**Risk Metrics**:

- Active risks count
- Mitigation effectiveness
- Issue resolution time

## Best Practices cho Team 2 Người

### 🤝 Collaboration

1. **Pair Programming**: Rotate giữa 2 developers
2. **Code Review**: Mandatory cho mọi pull request
3. **Knowledge Sharing**: Cross-training để backup
4. **Communication**: Daily sync, không chỉ standup

### 📊 Data Management

1. **Daily Updates**: Cập nhật progress hàng ngày
2. **Honest Estimation**: Realistic story points
3. **Track Actuals**: Ghi nhận actual hours
4. **Learn from Data**: Sử dụng metrics để improve

### 🎯 Focus & Prioritization

1. **Sprint Goal**: Luôn focus vào sprint goal
2. **Scope Management**: Tránh scope creep
3. **Technical Debt**: Allocate time cho refactoring
4. **Quality First**: Không compromise quality vì speed

## Customization và Mở Rộng

### Thêm User Stories Mới

1. Mở sheet "Product Backlog"
2. Thêm row mới với format chuẩn
3. Assign priority và story points
4. Update sprint planning nếu cần

### Thêm Risks Mới

1. Mở sheet "Risk Management"
2. Thêm risk với ID mới
3. Assess probability và impact
4. Define mitigation strategy

### Modify Sprint Timeline

1. Adjust dates trong "Sprint Planning"
2. Update capacity planning
3. Reschedule retrospectives

## Troubleshooting

### Khi Team Member Nghỉ

1. Check "Risk Management" cho mitigation plans
2. Redistribute tasks trong "Product Backlog"
3. Adjust capacity trong "Team Capacity Planning"
4. Update sprint scope nếu cần

### Khi Sprint Bị Delay

1. Analyze burndown data
2. Identify blockers trong daily scrum
3. Adjust scope hoặc extend sprint
4. Document lessons learned

### Khi Requirements Thay Đổi

1. Update User Stories trong backlog
2. Re-prioritize với stakeholders
3. Adjust sprint planning
4. Communicate impact lên team

## Kết Luận

File Excel này được thiết kế để hỗ trợ tối đa cho team 2 người trong việc áp dụng Scrum một cách hiệu quả. Với cấu trúc rõ ràng, màu sắc trực quan và các template sẵn có, team có thể tập trung vào development thay vì quản lý process.

**Lưu ý quan trọng**:

- Cập nhật data thường xuyên để có insights chính xác
- Sử dụng retrospective để cải tiến liên tục
- Adapt process theo nhu cầu cụ thể của team
- Maintain communication tốt giữa 2 team members

---

**Tác giả**: AI Assistant  
**Ngày tạo**: 2024  
**Phiên bản**: 1.0  
**Dự án**: Volunteer Management System
