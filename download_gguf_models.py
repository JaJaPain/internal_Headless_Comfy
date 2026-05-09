import os
from huggingface_hub import hf_hub_download

def download_models():
    base_path = os.path.join("ComfyUI_Backend", "models")
    
    # 1. Wan 2.1 14B I2V GGUF (The Brain)
    print("Downloading Wan 2.1 14B I2V GGUF (480P)...")
    diffusion_path = os.path.join(base_path, "diffusion_models")
    os.makedirs(diffusion_path, exist_ok=True)
    hf_hub_download(
        repo_id="city96/Wan2.1-I2V-14B-480P-gguf",
        filename="wan2.1-i2v-14b-480p-Q4_K_M.gguf",
        local_dir=diffusion_path
    )

    # 2. T5-XXL GGUF (The Instruction Reader)
    # city96/t5-v1_1-xxl-encoder-gguf/t5-v1_1-xxl-encoder-f16.gguf (or Q5_K_M)
    print("Downloading T5-XXL GGUF...")
    text_encoder_path = os.path.join(base_path, "text_encoders")
    os.makedirs(text_encoder_path, exist_ok=True)
    hf_hub_download(
        repo_id="city96/t5-v1_1-xxl-encoder-gguf",
        filename="t5-v1_1-xxl-encoder-Q5_K_M.gguf",
        local_dir=text_encoder_path
    )

    # 3. Wan 2.1 VAE
    print("Downloading Wan 2.1 VAE...")
    vae_path = os.path.join(base_path, "vae")
    os.makedirs(vae_path, exist_ok=True)
    hf_hub_download(
        repo_id="Wan-AI/Wan2.1-I2V-14B-480P",
        filename="Wan2.1_VAE.pth",
        local_dir=vae_path
    )

    # 4. CLIP (Image Encoder)
    print("Downloading CLIP Vision model...")
    clip_path = os.path.join(base_path, "clip")
    os.makedirs(clip_path, exist_ok=True)
    hf_hub_download(
        repo_id="Wan-AI/Wan2.1-I2V-14B-480P",
        filename="models_clip_open-clip-xlm-roberta-large-vit-huge-14.pth",
        local_dir=clip_path
    )

    # 5. Upscaler (4x-UltraSharp)
    print("Downloading 4x-UltraSharp Upscaler...")
    upscale_path = os.path.join(base_path, "upscale_models")
    os.makedirs(upscale_path, exist_ok=True)
    hf_hub_download(
        repo_id="lokCX/4x-Ultrasharp",
        filename="4x-UltraSharp.pth",
        local_dir=upscale_path
    )

    print("\nAll models (including Upscaler) downloaded successfully!")

if __name__ == "__main__":
    download_models()
