# Video Forge API Usage Guide

This document describes how to communicate with the decoupled Video Generation system from your main project.

## Endpoint: POST `/generate`

The primary endpoint for generating character animations.

### Parameters (Multipart Form Data)
- **`image`**: The character sprite image file (PNG/JPG).
- **`prompt`**: Text describing the motion (e.g., "A character walking in place").
- **`num_frames`**: (Optional) Number of frames to generate (Default: 16).
- **`seed`**: (Optional) Random seed for reproducible results (Default: 42).

### Example Call (Python)
```python
import requests

url = "http://localhost:8001/generate"
files = {'image': open('character.png', 'rb')}
data = {
    'prompt': 'A character performing a walking loop, stationary and centered',
    'num_frames': 16
}

response = requests.post(url, files=files, data=data)
with open('animation.mp4', 'wb') as f:
    f.write(response.content)
```

### Response
- **Success**: A binary stream of the generated MP4 video.
- **Error**: JSON object with error details.

## Why this is decoupled?
The `VideoCreation` folder contains its own isolated Python environment and a **Headless ComfyUI** engine. This ensures that:
1. Your main project stays small and doesn't need to install 20GB of AI libraries.
2. High RAM usage from the AI model won't crash your main application.
3. You can update the animation model (e.g., switching to a better version) without changing a single line of your core game code.

---

## Endpoint: POST `/upscale`

**Purpose:** Enhances low-res sprites into high-definition 4x-UltraSharp versions.

### Parameters (Multipart Form-Data)
- **`image`**: The sprite or image to upscale.

### Example Call (Python)
```python
import requests

with open("character.png", "rb") as f:
    response = requests.post(
        "http://localhost:8001/upscale",
        files={"image": f}
    )

with open("character_4x.png", "wb") as f:
    f.write(response.content)
```

## System Management
- **Startup**: Double-click **`run_everything.bat`**.
- **Engine**: ComfyUI runs on port `8188` (Internal, headless).
- **Frontend/API**: Bridge Server runs on port `8001` (Public).
