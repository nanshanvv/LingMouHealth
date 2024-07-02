import os
import json
import matplotlib
matplotlib.use('agg')

import torch
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt

from main_model import HiFuse_Base  # 引入你的模型定义文件并导入模型类

# Model saved with PyTorch torch.save()
MODEL_PATH = './models/best_model.pth'
model = HiFuse_Base(num_classes=8)  # 根据需要初始化你的模型

if os.path.exists(MODEL_PATH):
    # 文件存在，加载模型状态字典
    checkpoint = torch.load(MODEL_PATH)
    model.load_state_dict(checkpoint, strict=False)  # 直接加载整个检查点
    model.eval()
    print("模型加载成功！")
else:
    # 文件不存在，输出提示信息
    print(f"模型文件 '{MODEL_PATH}' 不存在。")

# 类名
class_names = ['AMD', 'CNV', 'CSR', 'DME', 'DR', 'DRUSEN', 'MH']
# 设置图片大小
img_width, img_height = 256, 256

def convert_to_rgb(img):
    # 如果图像已经是三通道，则无需转换
    if img.mode == 'RGB':
        return img

    # 创建一个新的三通道图像
    rgb_img = Image.new("RGB", img.size)

    # 将单通道图像复制三次以填充RGB通道
    rgb_img.paste(img)
    return rgb_img

def model_predict(img_path, model):
    # Open the image
    img = Image.open(img_path)
    img = convert_to_rgb(img)
    # Resize the image to match the model's input size
    img_size = 224
    data_transform = transforms.Compose([
        transforms.Resize(img_size),
        transforms.CenterCrop(img_size),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    ])

    img = data_transform(img)

    if img.dim() == 2:
        img = img.unsqueeze(0)

    # Expand batch dimension
    img = torch.unsqueeze(img, dim=0)

    # Move the tensor to the appropriate device (CPU or GPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    img = img.to(device)
    model = model.to(device)

    # Perform inference
    with torch.no_grad():
        preds = model(img)

    # Move the predictions back to CPU and flatten the array
    preds = preds.cpu().numpy().flatten()

    output_str = ""
    output_str += f"Predictions type: {type(preds)}\n"

    # new
    json_path = 'models/class_indices.json'
    assert os.path.exists(json_path), "file: '{}' does not exist.".format(json_path)

    with open(json_path, "r") as json_file:
        class_indict = json.load(json_file)

    with torch.no_grad():
        # predict class
        output = torch.squeeze(model(img.to(device))).cpu()
        predict = torch.softmax(output, dim=0)
        predict_cla = torch.argmax(predict).numpy()

    print_res = "class: {}   prob: {:.3}".format(class_indict[str(predict_cla)],
                                                 predict[predict_cla].numpy())
    plt.title(print_res)
    for i in range(len(predict)):
        output_str += "class: {:10}   prob: {:.3}\n".format(class_indict[str(i)], predict[i].numpy())

    max_class_name = class_indict[str(predict_cla)]
    max_class_prob = predict[predict_cla].numpy()

    output_str += "Most likely class: {:10}   Probability: {:.3}\n".format(max_class_name, max_class_prob)

    # Determine the class with the highest probability
    result = max_class_name

    # Return the prediction result, the path to the uploaded image, and the output string
    return result, img_path, output_str

# Example usage
# result, img_path, output_str = model_predict('path_to_image.jpg', model)
# print(output_str)
