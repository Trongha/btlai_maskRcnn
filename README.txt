
Hướng dẫn train:
  Chạy file rcnnMassk-Ship\samples\ship\ship.py với các tùy chọn như sau:
    --dataset= đường dẫn đến thư mục chứa dataset
    --weights= coco nếu train từ đầu.
	       last nếu train tiếp từ lần trước.
    ví dụ: 
	python ship.py train --dataset=../../datasets/ship --weights=coco

Hướng dẫn test:
  Chạy file inspect_custom_model
  Dữ liệu test trong folder: rcnnMassk-Ship\datasets\ship\val\
  Kết quả được lưu trong folder: rcnnMassk-Ship\samples\ship\imgSave\