import configparser
import io
import os
import tempfile
import http.client
import json
import base64
import numpy as np
import requests
import torch
from PIL import Image

class FalConfig:
    """Singleton class to handle API configuration and client setup."""
    _instance = None
    _key = None
    _imgbb_key = None  #ImgBB API密钥
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FalConfig, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize configuration and API key."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        config_path = os.path.join(parent_dir, "config.ini")
        config = configparser.ConfigParser()
        config.read(config_path)
        try:
            if os.environ.get("API_KEY") is not None:
                print("API_KEY found in environment variables")
                self._key = os.environ["API_KEY"]
            else:
                print("API_KEY not found in environment variables")
                self._key = config["API"]["API_KEY"]
                print("API_KEY found in config.ini")
                os.environ["API_KEY"] = self._key
                print("API_KEY set in environment variables")
            
            # 处理ImgBB API密钥
            if os.environ.get("IMGBB_API_KEY") is not None:
                print("IMGBB_API_KEY found in environment variables")
                self._imgbb_key = os.environ["IMGBB_API_KEY"]
            else:
                print("IMGBB_API_KEY not found in environment variables")
                try:
                    self._imgbb_key = config["API"]["IMGBB_API_KEY"]
                    print("IMGBB_API_KEY found in config.ini")
                    os.environ["IMGBB_API_KEY"] = self._imgbb_key
                    print("IMGBB_API_KEY set in environment variables")
                except KeyError:
                    print("Warning: IMGBB_API_KEY not found in config.ini")
                    self._imgbb_key = None
            
            
            if self._key == "<your_api_key_here>":
                print("WARNING: You are using the default API key placeholder!")
                print("Please set your actual API key in either:")
                print("1. The config.ini file under [API] section")
                print("2. Or as an environment variable named API_KEY")
            
            # 检查ImgBB API密钥
            if self._imgbb_key == "<your_imgbb_api_key_here>" or self._imgbb_key is None:
                print("WARNING: ImgBB API key not configured!")
                print("Please set your ImgBB API key in either:")
                print("1. The config.ini file under [API] section as IMGBB_API_KEY")
                print("2. Or as an environment variable named IMGBB_API_KEY")
                
        except KeyError:
            print("Error: API_KEY not found in config.ini or environment variables")
    
    def get_key(self):
        """Get the API key."""
        return self._key
    
    # 获取ImgBB API密钥方法
    def get_imgbb_key(self):
        """Get the ImgBB API key."""
        return self._imgbb_key

# ImgBB上传器类
class ImgBBUploader:
    """Class to handle ImgBB image uploads."""
    
    @staticmethod
    def upload_image(image, name="uploaded_image", expiration=None):
        """
        Upload image to ImgBB and return the URL.
        
        Args:
            image: PIL Image, numpy array, or torch tensor
            name: Name for the uploaded image
            expiration: Expiration time in seconds (60-15552000, optional)
        
        Returns:
            str: URL of uploaded image, or None if failed
        """
        try:
            # Convert image to base64
            base64_image = ImageUtils.image_to_base64(image)
            if not base64_image:
                print("Error: Failed to convert image to base64 for ImgBB upload")
                return None
            
            # Get ImgBB API key
            api_key = FalConfig().get_imgbb_key()
            if not api_key or api_key == "<your_imgbb_api_key_here>":
                print("Error: Invalid ImgBB API key")
                return None
            
            # Prepare upload data
            url = "https://api.imgbb.com/1/upload"
            payload = {
                "key": api_key,
                "image": base64_image,
                "name": name
            }
            
            if expiration:
                payload["expiration"] = expiration
            
            # Upload to ImgBB
            print(f"Uploading image to ImgBB...")
            response = requests.post(url, data=payload)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    image_url = result["data"]["url"]
                    print(f"Image uploaded successfully: {image_url}")
                    return image_url
                else:
                    print(f"ImgBB upload failed: {result.get('error', {}).get('message', 'Unknown error')}")
                    return None
            else:
                print(f"ImgBB upload failed with status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error uploading to ImgBB: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

class ImageUtils:
    """Utility functions for image processing."""
    @staticmethod
    def tensor_to_pil(image):
        """Convert image tensor to PIL Image."""
        try:
            
            if isinstance(image, torch.Tensor):
                image_np = image.cpu().numpy()
            else:
                image_np = np.array(image)
            
            if image_np.ndim == 4:
                image_np = image_np.squeeze(0)  
            if image_np.ndim == 2:
                image_np = np.stack([image_np] * 3, axis=-1)  
            elif image_np.shape[0] == 3:
                image_np = np.transpose(
                    image_np, (1, 2, 0)
                )  
            
            if image_np.dtype == np.float32 or image_np.dtype == np.float64:
                image_np = (image_np * 255).astype(np.uint8)
            
            return Image.fromarray(image_np)
        except Exception as e:
            print(f"Error converting tensor to PIL: {str(e)}")
            return None
    @staticmethod
    def image_to_base64(image):
        """Convert image tensor to base64 string."""
        try:
            print(f"开始转换图像，输入类型: {type(image)}")
            print(f"输入形状: {image.shape if hasattr(image, 'shape') else '无shape属性'}")
            print(f"输入数据类型: {image.dtype if hasattr(image, 'dtype') else '无dtype属性'}")
            
            pil_image = ImageUtils.tensor_to_pil(image)
            
            if not pil_image:
                print("Error: tensor_to_pil 返回了 None 或空值")
                return None
            
            print(f"PIL图像转换成功，模式: {pil_image.mode}, 尺寸: {pil_image.size}")
            
            buffered = io.BytesIO()
            pil_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            print(f"Base64转换成功，长度: {len(img_str)}")
            return img_str
        
        except Exception as e:
            print(f"Error converting image to base64: {str(e)}")
            import traceback
            traceback.print_exc()  # 打印完整的错误堆栈
            return None

    
    @staticmethod
    def image_to_url(image, name="uploaded_image", expiration=None):
        """Convert image tensor to URL using ImgBB."""
        try:
            print(f"开始上传图像到ImgBB，输入类型: {type(image)}")
            
            
            image_url = ImgBBUploader.upload_image(image, name, expiration)
            
            if image_url:
                print(f"图像上传成功，URL: {image_url}")
                return image_url
            else:
                print("Error: 图像上传失败")
                return None
        
        except Exception as e:
            print(f"Error converting image to URL: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    @staticmethod
    def mask_to_image(mask):
        """Convert mask tensor to image tensor."""
        result = (
            mask.reshape((-1, 1, mask.shape[-2], mask.shape[-1]))
            .movedim(1, -1)
            .expand(-1, -1, -1, 3)
        )
        return result

class ResultProcessor:
    """Utility functions for processing API results."""
    @staticmethod
    def process_image_result(result):
        """Process image generation result and return tensor."""
        try:
            images = []
            
            
            if "data" in result and len(result["data"]) > 0:
                for img_info in result["data"]:
                    if "url" in img_info:
                        img_url = img_info["url"]
                        img_response = requests.get(img_url)
                        img = Image.open(io.BytesIO(img_response.content))
                        img_array = np.array(img).astype(np.float32) / 255.0
                        images.append(img_array)
            elif "images" in result:
                
                for img_info in result["images"]:
                    img_url = img_info["url"]
                    img_response = requests.get(img_url)
                    img = Image.open(io.BytesIO(img_response.content))
                    img_array = np.array(img).astype(np.float32) / 255.0
                    images.append(img_array)
            if not images:
                return ResultProcessor.create_blank_image()
            
            stacked_images = np.stack(images, axis=0)
            
            img_tensor = torch.from_numpy(stacked_images)
            return (img_tensor,)
        except Exception as e:
            print(f"Error processing image result: {str(e)}")
            return ResultProcessor.create_blank_image()
    @staticmethod
    def process_single_image_result(result):
        """Process single image result and return tensor."""
        try:
            
            if "data" in result and len(result["data"]) > 0:
                img_url = result["data"][0]["url"]
            elif "image" in result:
                img_url = result["image"]["url"]
            else:
                return ResultProcessor.create_blank_image()
                
            img_response = requests.get(img_url)
            img = Image.open(io.BytesIO(img_response.content))
            img_array = np.array(img).astype(np.float32) / 255.0
            
            stacked_images = np.stack([img_array], axis=0)
            
            img_tensor = torch.from_numpy(stacked_images)
            return (img_tensor,)
        except Exception as e:
            print(f"Error processing single image result: {str(e)}")
            return ResultProcessor.create_blank_image()
    @staticmethod
    def create_blank_image():
        """Create a blank black image tensor."""
        blank_img = Image.new("RGB", (512, 512), color="black")
        img_array = np.array(blank_img).astype(np.float32) / 255.0
        img_tensor = torch.from_numpy(img_array)[None,]
        return (img_tensor,)

class ApiHandler:
    """Utility functions for API interactions."""
    @staticmethod
    def submit_and_get_result(model_name, arguments):
        """Submit job to your chat API and get result."""
        try:
            
            payload_data = {
                "model": model_name,
                **arguments
            }
            
            
            conn = http.client.HTTPSConnection("api.tu-zi.com")
            payload = json.dumps(payload_data, ensure_ascii=False).encode('utf-8')
            
            
            headers = {
                'Authorization': f'Bearer {FalConfig().get_key()}',
                'Content-Type': 'application/json; charset=utf-8'
            }
            
            
            conn.request("POST", "/v1/images/generations", payload, headers)
            res = conn.getresponse()
            data = res.read()
            
            
            result = json.loads(data.decode("utf-8"))
            conn.close()
            
            return result
            
        except Exception as e:
            print(f"Error submitting to {model_name}: {str(e)}")
            raise e
    @staticmethod
    def handle_video_generation_error(model_name, error):
        """Handle video generation errors consistently."""
        print(f"Error generating video with {model_name}: {str(error)}")
        return ("Error: Unable to generate video.",)
    @staticmethod
    def handle_image_generation_error(model_name, error):
        """Handle image generation errors consistently."""
        print(f"Error generating image with {model_name}: {str(error)}")
        return ResultProcessor.create_blank_image()
    @staticmethod
    def handle_text_generation_error(model_name, error):
        """Handle text generation errors consistently."""
        print(f"Error generating text with {model_name}: {str(error)}")
        return ("Error: Unable to generate text.",)