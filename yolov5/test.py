import torch
import torchvision.transforms as transforms
from PIL import Image

model_path = 'C:/Users/Jeong/Desktop/yolo_test/yolov5/runs/train/pet_yolov5s_results/weights/best.pt'
checkpoint = torch.load(model_path)  # 딕셔너리로 모델 로드

model = checkpoint['model'].float()  # 모델 추출
model.eval()  # 모델을 평가 모드로 설정

preprocess = transforms.Compose([
    transforms.Resize((640, 640)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

img = Image.open('C:/Users/Jeong/Desktop/york.jpg')
preprocessed_img = preprocess(img).unsqueeze(0)  # 배치 차원 추가

with torch.no_grad():
    results = model(preprocessed_img)

boxes = results[0][0][:, :4]  # 바운딩 박스 좌표
scores = results[0][0][:, 4]  # 예측 점수
classes = results[0][0][:, 5]  # 예측된 클래스

print("bounding:",boxes)
print("scores:",scores)
print("classes",classes)

# 박스와 클래스 정보를 시각화하여 이미지에 적용
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

plt.figure()
plt.imshow(img)
ax = plt.gca()

# 상위 몇 개의 객체만 시각화 (상위 100개 등)
for box, score, cls in zip(boxes[:100], scores[:100], classes[:100]):
    box = box.cpu().numpy()
    rect = Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1], fill=False, edgecolor='r', linewidth=1)
    ax.add_patch(rect)
    plt.text(box[0], box[1], f'Class {int(cls)}', bbox=dict(facecolor='red', alpha=0.5))

plt.show()