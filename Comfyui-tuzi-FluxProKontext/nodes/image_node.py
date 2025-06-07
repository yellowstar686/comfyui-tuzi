from .fal_utils import ApiHandler, ImageUtils, ResultProcessor

def upload_image(image):
    """Upload image tensor to FAL and return URL."""
    return ImageUtils.upload_image(image)


class FluxProKontext:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image": ("IMAGE",),
            },
            "optional": {
                "aspect_ratio": (
                    [
                        None,
                        "21:9",
                        "16:9",
                        "4:3",
                        "3:2",
                        "1:1",
                        "2:3",
                        "3:4",
                        "9:16",
                        "9:21",
                    ],
                    {"default": "16:9"},
                ),
                "output_format": (["jpeg", "png"], {"default": "png"}),
                "safety_tolerance": (["1", "2", "3", "4", "5", "6"], {"default": "2"}),
                "prompt_upsampling": ("BOOLEAN", {"default": False}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**32 - 1}),
                "model": (["flux-kontext-pro", "flux-kontext-max"], {"default": "flux-kontext-pro"}),
            },
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"
    CATEGORY = "TuZi/Image"
    
    def generate_image(
        self,
        prompt,
        image,
        aspect_ratio="16:9",
        output_format="png",
        safety_tolerance="2",
        prompt_upsampling=False,
        seed=0,
        model="flux-kontext-pro"
    ):
        
        valid_models = ["flux-kontext-pro", "flux-kontext-max"]
        if model not in valid_models:
            print(f"Warning: Invalid model {model}, using default flux-kontext-pro")
            model = "flux-kontext-pro"
        
        
        input_image_url = ImageUtils.image_to_url(
            image,
            name=f"flux_kontext_input_{hash(str(prompt))}",
            expiration=None  # 不设置过期时间
        )
        if not input_image_url:
            print("Error: Failed to upload input image to ImgBB")
            return ResultProcessor.create_blank_image()
        print(f"Input image uploaded successfully: {input_image_url}")
        
        
        combined_prompt = f"{input_image_url} {prompt}"
        
        
        arguments = {
            "prompt": combined_prompt,  # 合并后的prompt
            "aspect_ratio": aspect_ratio,
            "output_format": output_format,
            "safety_tolerance": int(safety_tolerance),
            "prompt_upsampling": prompt_upsampling,
        }
        
        if seed > 0:
            arguments["seed"] = seed
        
        try:
            print(f"Using model: {model}")
            result = ApiHandler.submit_and_get_result(model, arguments)
            return ResultProcessor.process_image_result(result)
        except Exception as e:
            return ApiHandler.handle_image_generation_error("Flux Pro Kontext", e)

# FluxProKontextMulti - 多图像输入的Kontext模型
class FluxProKontextMulti:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "image_1": ("IMAGE",),
                "image_2": ("IMAGE",),
            },
            "optional": {
                "image_3": ("IMAGE",),
                "image_4": ("IMAGE",),
                "aspect_ratio": (
                    [
                        None,
                        "21:9",
                        "16:9",
                        "4:3",
                        "3:2",
                        "1:1",
                        "2:3",
                        "3:4",
                        "9:16",
                        "9:21",
                    ],
                    {"default": "16:9"},
                ),
                "output_format": (["jpeg", "png"], {"default": "png"}),
                "safety_tolerance": (["1", "2", "3", "4", "5", "6"], {"default": "2"}),
                "prompt_upsampling": ("BOOLEAN", {"default": False}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**32 - 1}),
                "model": (["flux-kontext-pro", "flux-kontext-max"], {"default": "flux-kontext-pro"}),
            },
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"
    CATEGORY = "TuZi/Image"
    
    def generate_image(
        self,
        prompt,
        image_1,
        image_2,
        image_3=None,
        image_4=None,
        aspect_ratio="16:9",
        output_format="png",
        safety_tolerance="2",
        prompt_upsampling=False,
        seed=0,
        model="flux-kontext-pro"
    ):
        
        valid_models = ["flux-kontext-pro", "flux-kontext-max"]
        if model not in valid_models:
            print(f"Warning: Invalid model {model}, using default flux-kontext-pro")
            model = "flux-kontext-pro"
        
        
        image_urls = []
        images_to_upload = [image_1, image_2, image_3, image_4]
        
        for i, img in enumerate(images_to_upload, 1):
            if img is not None:
                
                url = ImageUtils.image_to_url(
                    img,
                    name=f"flux_kontext_multi_input_{i}_{hash(str(prompt))}",
                    expiration=None  # 不设置过期时间
                )
                if url:
                    image_urls.append(url)
                    print(f"Image {i} uploaded successfully: {url}")
                else:
                    print(f"Error: Failed to upload image {i} to ImgBB")
                    return ResultProcessor.create_blank_image()
        
        if len(image_urls) < 2:
            print("Error: At least 2 images required for Flux Pro Kontext Multi")
            return ResultProcessor.create_blank_image()
        
        urls_string = " ".join(image_urls)
        combined_prompt = f"{urls_string} {prompt}"
        
        
        arguments = {
            "prompt": combined_prompt,  # 合并后的prompt
            "aspect_ratio": aspect_ratio,
            "output_format": output_format,
            "safety_tolerance": int(safety_tolerance),
            "prompt_upsampling": prompt_upsampling,
        }
        
        if seed > 0:
            arguments["seed"] = seed
        
        try:
            print(f"Using model: {model}")
            result = ApiHandler.submit_and_get_result(model, arguments)
            return ResultProcessor.process_image_result(result)
        except Exception as e:
            return ApiHandler.handle_image_generation_error("Flux Pro Kontext Multi", e)


# FluxProKontextTextToImage - 纯文生图的Kontext模型
class FluxProKontextTextToImage:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
            },
            "optional": {
                "aspect_ratio": (
                    ["21:9", "16:9", "4:3", "3:2", "1:1", "2:3", "3:4", "9:16", "9:21"],
                    {"default": "16:9"},
                ),
                "output_format": (["jpeg", "png"], {"default": "png"}),
                "safety_tolerance": (["1", "2", "3", "4", "5", "6"], {"default": "2"}),
                "prompt_upsampling": ("BOOLEAN", {"default": False}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**32 - 1}),
                "model": (["flux-kontext-pro", "flux-kontext-max"], {"default": "flux-kontext-pro"}),
            },
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate_image"
    CATEGORY = "TuZi/Image"
    
    def generate_image(
        self,
        prompt,
        aspect_ratio="16:9",
        output_format="png",
        safety_tolerance="2",
        prompt_upsampling=False,
        seed=0,
        model="flux-kontext-pro"
    ):
        
        valid_models = ["flux-kontext-pro", "flux-kontext-max"]
        if model not in valid_models:
            print(f"Warning: Invalid model {model}, using default flux-kontext-pro")
            model = "flux-kontext-pro"
        
        arguments = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "output_format": output_format,
            "safety_tolerance": int(safety_tolerance),
            "prompt_upsampling": prompt_upsampling,
        }
        
        if seed > 0:
            arguments["seed"] = seed
        
        try:
            print(f"Using model: {model}")
            result = ApiHandler.submit_and_get_result(model, arguments)
            return ResultProcessor.process_image_result(result)
        except Exception as e:
            return ApiHandler.handle_image_generation_error("Flux Pro Kontext Text-to-Image", e)

NODE_CLASS_MAPPINGS = {
    "FluxProKontext_fal": FluxProKontext,
    "FluxProKontextMulti_fal": FluxProKontextMulti,
    "FluxProKontextTextToImage_fal": FluxProKontextTextToImage,
}


NODE_DISPLAY_NAME_MAPPINGS = {
    "FluxProKontext_fal": "Flux-Pro-Kontext-i2i",
    "FluxProKontextMulti_fal": "Flux-Pro-Kontext-4i2i",
    "FluxProKontextTextToImage_fal": "Flux-Pro-Kontext-t2i",
}