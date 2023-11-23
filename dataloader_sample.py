import os #add圖片
from PIL import Image #add圖片
from torchvision import transforms #圖像進行預處理和轉換的函數
from torch.utils.data import Dataset, DataLoader #表示一個數據集和數據加載器，它提供了對數據集的高效迭代支持

class FruitDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        # 初始化數據集
        self.root_dir = root_dir
        self.transform = transform
        self.classes = sorted(os.listdir(root_dir))  # 獲取數據集中的類別名稱

        self.file_list = []
        for class_label in self.classes:
            class_path = os.path.join(root_dir, class_label)

            files = os.listdir(class_path)

            # 將每個樣本的類別標籤和文件名存儲在file_list中
            self.file_list.extend([(class_label, file) for file in files])

    def __len__(self):
        # 返回數據集的大小（樣本的數量）
        return len(self.file_list)

    def __getitem__(self, idx):
        # 根據索引返回單個樣本
        class_label, file_name = self.file_list[idx]
        img_path = os.path.join(self.root_dir, class_label, file_name)
        image = Image.open(img_path).convert('RGB')  # 打開並轉換圖像為RGB模式

        if self.transform:
            # 如果transform不為None，則應用轉換操作到圖像上
            image = self.transform(image)

        return image, class_label

# Example usage
#windows_path = r"C:\Users\rayso_sq9ff\Downloads\archive\train\train\Strawberry"
windows_path= r"C:\Users\rayso_sq9ff\Downloads\archive\train\train\Strawberry"
dataset_path = os.path.normpath(windows_path)
batch_size = 32

# Define transformations
data_transform = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize images to a fixed size
    transforms.ToTensor(),  # Convert images to PyTorch tensors
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])  # 对图像进行归一化处理
])

# Create the dataset
fruit_dataset = FruitDataset(root_dir=dataset_path, transform=data_transform)

# Create the DataLoader
fruit_loader = DataLoader(dataset=fruit_dataset, batch_size=batch_size, shuffle=True)

