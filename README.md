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
