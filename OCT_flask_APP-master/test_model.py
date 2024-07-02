import torch

# 加载两个模型文件
model_path_1 = "models/best_model.pth"


# 加载检查点
checkpoint1 = torch.load(model_path_1, map_location=torch.device('cpu'))


# 列出每个检查点中的键
keys_checkpoint1 = list(checkpoint1.keys())


# 打印检查点中的键
print("Keys in checkpoint1:", keys_checkpoint1)




