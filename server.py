import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from comfy_wrapper import ComfyWrapper
import uvicorn

app = FastAPI()
comfy = ComfyWrapper()

# Root route to serve the frontend
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r") as f:
        return f.read()

@app.post("/generate")
async def generate_video(
    image: UploadFile = File(...),
    prompt: str = Form(...),
    num_frames: int = Form(16),
    seed: int = Form(42)
):
    try:
        # 1. Save uploaded image temporarily
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, image.filename)
        
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            
        # 2. Call ComfyUI via our wrapper
        print(f"Requesting generation for: {prompt} ({num_frames} frames, seed: {seed})")
        video_path = comfy.generate_video(temp_path, prompt, num_frames=num_frames, seed=seed)
        
        # 3. Return the video file
        return FileResponse(video_path, media_type="video/mp4", filename="animation.mp4")
        
    except Exception as e:
        print(f"Error during generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upscale")
async def upscale_image(
    image: UploadFile = File(...)
):
    try:
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, image.filename)
        
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            
        print(f"Requesting upscale for: {image.filename}")
        upscaled_path = comfy.upscale_image(temp_path)
        
        return FileResponse(upscaled_path, media_type="image/png", filename="upscaled.png")
        
    except Exception as e:
        print(f"Error during upscale: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
