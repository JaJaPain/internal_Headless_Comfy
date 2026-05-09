import requests
import os

SERVER_URL = "http://127.0.0.1:8001"

def test_gen():
    print("Sending generation request (multipart/form-data)...")
    
    # Create a dummy image for testing
    dummy_image = "test_image.png"
    if not os.path.exists(dummy_image):
        with open(dummy_image, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdcD\x1e\xf7\x00\x00\x00\x00IEND\xaeB`\x82")

    files = {
        'image': ('test_image.png', open(dummy_image, 'rb'), 'image/png')
    }
    data = {
        'prompt': 'A character performing a walking loop, centered, green background',
        'num_frames': 33,
        'seed': 42
    }
    
    try:
        response = requests.post(f"{SERVER_URL}/generate", files=files, data=data)
        if response.status_code == 200:
            print("Generation successful!")
            with open("output_animation.mp4", "wb") as f:
                f.write(response.content)
            print("Saved to output_animation.mp4")
        else:
            print(f"Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_gen()
