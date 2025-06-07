# TuZi API - Flux Kontext Nodes

[English](#english) | [中文](#中文)

---

## English

### 🚀 Overview

TuZi API - Flux Kontext Nodes is a custom ComfyUI extension that provides powerful Flux Pro Kontext image generation capabilities. This project is adapted from the fal_api project and currently uses ImgBB for image uploading and integration.

### ⚠️ Important Notice

- **Image Upload**: Currently uses ImgBB for image uploading (temporary solution)
- **Free Tier Limit**: Non-member accounts can upload 100 images per hour for free
- **API Keys Required**: Both TuZi API key and ImgBB API key are required
- **Future Update**: Will be updated once TuZi supports base64 image upload

### 🔑 API Keys Setup

You need to obtain two API keys:

1. **TuZi API Key**: Get from [TuZi API Panel](https://api.tu-zi.com/panel)
2. **ImgBB API Key**: Get from [ImgBB](https://imgbb.com/)

### 📁 Configuration

Create a `config.ini` file in the plugin directory with your API keys:

```ini
[API]
API_KEY = your_tuzi_api_key_here
IMGBB_API_KEY = your_imgbb_api_key_here
📦 Installation
Method 1: Via ComfyUI Manager (Recommended)
Open ComfyUI Manager in your ComfyUI interface
Click "Install via Git URL"
Enter: https://github.com/yellowstar686/tuzi-api.git
Restart ComfyUI after installation
Method 2: Manual Installation
cd ComfyUI/custom_nodes
git clone https://github.com/yellowstar686/tuzi-api.git
cd tuzi-api
pip install -r requirements.txt
cd ComfyUI/custom_nodes
git clone https://github.com/yellowstar686/tuzi-api.git
cd tuzi-api
pip install -r requirements.txt
🎯 Usage
After installation, you'll find three new nodes under the "TuZi/Image" category:

1. Flux Pro Kontext (Single Image)
Input: Text prompt + Single image
Use Case: Image-to-image generation with context understanding
Parameters:
Prompt (text)
Input image
Aspect ratio (16:9, 1:1, etc.)
Output format (PNG/JPEG)
Safety tolerance
Prompt upsampling
2. Flux Pro Kontext Multi
Input: Text prompt + Multiple images (2-4)
Use Case: Complex scene generation using multiple reference images
Parameters:
Prompt (text)
Image 1-4 (at least 2 required)
Aspect ratio
Output format
Safety tolerance
Prompt upsampling
3. Flux Pro Kontext Text-to-Image
Input: Text prompt only
Use Case: Pure text-based image generation
Parameters:
Prompt (text)
Aspect ratio
Output format
Safety tolerance
Prompt upsampling
🔧 Configuration Notes
Internal Use: API keys are stored in config.ini for convenient internal platform usage
Manual Setup: You need to manually fill in the API keys in the configuration file
Temporary Solution: ImgBB integration is temporary until TuZi supports base64 image upload
📋 Requirements
Python >= 3.8
ComfyUI
torch
requests
Pillow
numpy
🐛 Troubleshooting
Node not appearing?

Restart ComfyUI completely
Check if config.ini file exists with correct API keys
Verify the installation in ComfyUI/custom_nodes/tuzi-api
API errors?

Check your TuZi API key validity
Verify ImgBB API key is correct
Check API quota limits
Check ComfyUI console for detailed error messages
Image upload failures?

Ensure input images are valid formats (PNG, JPEG)
Check ImgBB upload limit (100 images/hour for free accounts)
Verify internet connection
🔮 Future Updates
Will be updated once TuZi API supports base64 image upload
ImgBB dependency will be removed in future versions
Enhanced error handling and user experience improvements
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

📞 Support
Issues: GitHub Issues
Documentation: GitHub Repository
中文
🚀 概述
TuZi API - Flux Kontext 节点是一个自定义的 ComfyUI 扩展，提供强大的 Flux Pro Kontext 图像生成功能。该项目改自 fal_api 项目，目前通过 ImgBB 负责图像上传和整合。

⚠️ 重要说明
图像上传: 目前使用 ImgBB 进行图像上传（临时方案）
免费限制: 非会员账户每小时可免费上传 100 张图片
API 密钥: 需要 TuZi API 密钥和 ImgBB API 密钥
未来更新: 待 TuZi 支持 base64 图像上传后会更新项目
🔑 API 密钥设置
您需要获取两个 API 密钥：

TuZi API 密钥: 从 兔子API控制台 获取
ImgBB API 密钥: 从 ImgBB 获取
📁 配置文件
在插件目录中创建 config.ini 文件，填入您的 API 密钥：

[API]
API_KEY = 您的兔子API密钥
IMGBB_API_KEY = 您的ImgBB_API密钥
📦 安装方法
方法一：通过 ComfyUI Manager 安装（推荐）
在 ComfyUI 界面中打开 ComfyUI Manager
点击 "Install via Git URL"
输入：https://github.com/yellowstar686/tuzi-api.git
安装完成后重启 ComfyUI
方法二：手动安装
cd ComfyUI/custom_nodes
git clone https://github.com/yellowstar686/tuzi-api.git
cd tuzi-api
pip install -r requirements.txt
cd ComfyUI/custom_nodes
git clone https://github.com/yellowstar686/tuzi-api.git
cd tuzi-api
pip install -r requirements.txt
🎯 使用方法
安装完成后，您将在 "TuZi/Image" 分类下找到三个新节点：

1. Flux Pro Kontext（单图像）
输入: 文本提示词 + 单张图像
用途: 基于上下文理解的图像到图像生成
参数:
提示词（文本）
输入图像
宽高比（16:9, 1:1 等）
输出格式（PNG/JPEG）
安全等级
提示词增强
2. Flux Pro Kontext Multi（多图像）
输入: 文本提示词 + 多张图像（2-4张）
用途: 使用多个参考图像生成复杂场景
参数:
提示词（文本）
图像 1-4（至少需要2张）
宽高比
输出格式
安全等级
提示词增强
3. Flux Pro Kontext Text-to-Image（文生图）
输入: 仅文本提示词
用途: 纯文本生成图像
参数:
提示词（文本）
宽高比
输出格式
安全等级
提示词增强
🔧 配置说明
内部使用: API 密钥存储在 config.ini 中，方便作为内部平台使用
手动配置: 需要手动在配置文件中填写 API 密钥
临时方案: ImgBB 集成是临时方案，待 TuZi 支持 base64 图像上传后会更新
📋 系统要求
Python >= 3.8
ComfyUI
torch
requests
Pillow
numpy
🐛 故障排除
节点没有出现？

完全重启 ComfyUI
检查 config.ini 文件是否存在且包含正确的 API 密钥
验证安装位置：ComfyUI/custom_nodes/tuzi-api
API 错误？

检查 TuZi API 密钥是否有效
验证 ImgBB API 密钥是否正确
检查 API 配额限制
查看 ComfyUI 控制台的详细错误信息
图像上传失败？

确保输入图像格式有效（PNG, JPEG）
检查 ImgBB 上传限制（免费账户每小时 100 张）
验证网络连接
🔮 未来更新
待 TuZi API 支持 base64 图像上传后会更新项目
未来版本将移除 ImgBB 依赖
增强错误处理和用户体验改进
📄 许可证
本项目采用 MIT 许可证 - 详见 LICENSE 文件。

🤝 贡献
欢迎贡献！请随时提交 Pull Request。

📞 支持
问题反馈: GitHub Issues
项目文档: GitHub 仓库
