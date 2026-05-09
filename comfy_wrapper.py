import json
import urllib.request
import urllib.parse
import uuid
import os
import time
import requests

class ComfyWrapper:
    def __init__(self, server_address="127.0.0.1:8188"):
        self.server_address = server_address
        self.client_id = str(uuid.uuid4())

    def queue_prompt(self, prompt):
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{self.server_address}/prompt", data=data)
        return json.loads(urllib.request.urlopen(req).read())

    def get_history(self, prompt_id):
        with urllib.request.urlopen(f"http://{self.server_address}/history/{prompt_id}") as response:
            return json.loads(response.read())

    def upload_image(self, image_path):
        url = f"http://{self.server_address}/upload/image"
        with open(image_path, "rb") as f:
            files = {"image": (os.path.basename(image_path), f)}
            response = requests.post(url, files=files)
            return response.json()

    def generate_video(self, image_path, prompt_text, num_frames=16, seed=42, workflow_path="workflow_api.json"):
        # 1. Upload the reference image
        print(f"Uploading image {image_path} to ComfyUI...")
        upload_resp = self.upload_image(image_path)
        comfy_filename = upload_resp['name']

        # 2. Load and prepare the workflow
        with open(workflow_path, 'r') as f:
            workflow = json.load(f)

        # Update prompt (Node 16)
        workflow["16"]["inputs"]["positive_prompt"] = prompt_text
        # Update image (Node 58)
        workflow["58"]["inputs"]["image"] = comfy_filename
        # Update num_frames (Node 63)
        workflow["63"]["inputs"]["num_frames"] = num_frames
        # Update seed (Node 35)
        workflow["35"]["inputs"]["seed"] = seed

        # 3. Queue the prompt
        print("Queueing generation...")
        prompt_resp = self.queue_prompt(workflow)
        prompt_id = prompt_resp['prompt_id']

        # 4. Wait for completion
        print(f"Waiting for prompt {prompt_id} to complete...")
        while True:
            history = self.get_history(prompt_id)
            if prompt_id in history and history[prompt_id].get('outputs'):
                break
            time.sleep(2)

        # 5. Extract the output filename
        outputs = history[prompt_id]['outputs']
        # Node 30 is Video Combine (VHS) which uses 'gifs' key
        if 'gifs' in outputs['30']:
            video_output = outputs['30']['gifs'][0]
        else:
            # Fallback for other video nodes
            video_output = outputs['30'].get('filenames', [{}])[0]
            
        video_filename = video_output.get('filename')
        
        # 6. Download the result
        print(f"Downloading result: {video_filename}")
        video_url = f"http://{self.server_address}/view?filename={video_filename}&type=output"
        output_local_path = os.path.abspath(os.path.join("outputs", f"gen_{int(time.time())}.mp4"))
        os.makedirs("outputs", exist_ok=True)
        
        with urllib.request.urlopen(video_url) as response, open(output_local_path, 'wb') as out_file:
            out_file.write(response.read())

        return output_local_path

        return output_local_path

    def upscale_image(self, image_path, workflow_path="upscale_workflow_api.json"):
        # 1. Upload
        print(f"Uploading image {image_path} for upscaling...")
        upload_resp = self.upload_image(image_path)
        comfy_filename = upload_resp['name']

        # 2. Prepare workflow
        with open(workflow_path, 'r') as f:
            workflow = json.load(f)
        
        workflow["1"]["inputs"]["image"] = comfy_filename

        # 3. Queue
        print("Queueing upscale...")
        prompt_resp = self.queue_prompt(workflow)
        prompt_id = prompt_resp['prompt_id']

        # 4. Wait
        while True:
            history = self.get_history(prompt_id)
            if prompt_id in history and history[prompt_id].get('outputs'):
                break
            time.sleep(1)

        # 5. Extract output (Node 4)
        outputs = history[prompt_id]['outputs']
        image_output = outputs['4']['images'][0]
        image_filename = image_output['filename']

        # 6. Download
        print(f"Downloading upscaled image: {image_filename}")
        image_url = f"http://{self.server_address}/view?filename={image_filename}&type=output"
        output_local_path = os.path.abspath(os.path.join("outputs", f"upscale_{int(time.time())}.png"))
        os.makedirs("outputs", exist_ok=True)

        with urllib.request.urlopen(image_url) as response, open(output_local_path, 'wb') as out_file:
            out_file.write(response.read())

        return output_local_path

if __name__ == "__main__":
    wrapper = ComfyWrapper()
    # This assumes ComfyUI is already running
    # wrapper.generate_video("test_image.png", "A character walking loop")
