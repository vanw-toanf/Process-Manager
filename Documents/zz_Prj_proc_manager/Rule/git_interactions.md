# Git Commands Cheat Sheet

## Tạo Repository
- `git clone <repository_url>`  
  *Clone một repository từ remote*
- `git init`  
  *Khởi tạo một repository mới*
- `git remote add origin "link"`  
  *Kết nối kho từ xa*

## Lưu Tạm Thời Sửa Đổi
- `git add .`  
  *Thêm tất cả các thay đổi vào staging area*
- `git commit -m "Mô tả ngắn gọn về thay đổi"`  
  *Commit các thay đổi*

## Đẩy Lên Remote
- `git push origin <tên_nhánh>`  
  *Đẩy các thay đổi lên nhánh chính của remote*

## Kéo Về từ Remote
- `git fetch origin <tên_nhánh>`  
  *Kéo một bản trên repo về nhưng không hợp nhất*
- `git diff <tên nhánh> origin/<tên nhánh>`  
  *Kiểm tra sự khác biệt giữa 2 bản*  
  *Hoặc có thể dùng git log <tên nhánh>..origin/<tên nhánh> để xem nhanh các commit mới*  
- `git pull origin <tên_nhánh>`  
  *Kéo các thay đổi mới nhất từ remote về máy local*

## Quản Lý Branch
- `git branch -r`  
  *Liệt kê các nhánh repo*
- `git branch`  
  *Liệt kê các nhánh local*
- `git checkout -b <tên_nhánh_mới>`  
  *Tạo một nhánh mới và chuyển sang nhánh đó*
- `git checkout <tên_nhánh>`  
  *Chuyển đến một nhánh đã có*
- `git branch -d <tên_nhánh>`  
  *Xóa một nhánh local*
- `git push origin --delete <tên_nhánh>`  
  *Xóa nhánh trên GitHub*

## Xóa File
- `git rm <tên_file>`  
  *Xóa file khỏi repository (và cũng xóa khỏi local)*
- `git rm --cached <tên_file>`  
  *Xóa file khỏi repository nhưng giữ lại trong local*

## Hợp Nhất Branch
- `git checkout <tên_nhánh_đích>`  
  *Nhảy đến nhánh mà bạn muốn hợp nhất*
- `git merge <tên_nhánh_cần_hợp_nhất>`  
  *Hợp nhất một nhánh vào nhánh hiện tại*

## Kiểm Tra Trạng Thái Branch Hiện Tại
- `git status`  
  *Kiểm tra trạng thái hiện tại của repository*
- `git log <tên nhánh>..origin/<tên nhánh>`  
  *Kiểm tra có commit mới nào trên nhánh remote không*
  *Cần kêt hợp git fetch để cập nhật branch trước*
