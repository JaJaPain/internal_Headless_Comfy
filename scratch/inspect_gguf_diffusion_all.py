import gguf
import sys

def inspect_gguf(path):
    try:
        reader = gguf.GGUFReader(path)
        for tensor in reader.tensors:
            print(tensor.name)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    path = "ComfyUI_Backend/models/diffusion_models/wan2.1-i2v-14b-480p-Q4_K_M.gguf"
    inspect_gguf(path)
