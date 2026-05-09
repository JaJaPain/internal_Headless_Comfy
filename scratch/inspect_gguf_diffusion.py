import gguf
import sys

def inspect_gguf(path):
    try:
        reader = gguf.GGUFReader(path)
        print(f"Inspecting GGUF: {path}")
        print(f"Tensor count: {len(reader.tensors)}")
        for i, tensor in enumerate(reader.tensors):
            if i < 20:
                print(f"Tensor {i}: {tensor.name}")
            elif i == 20:
                print("...")
            elif i > len(reader.tensors) - 5:
                print(f"Tensor {i}: {tensor.name}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    path = "ComfyUI_Backend/models/diffusion_models/wan2.1-i2v-14b-480p-Q4_K_M.gguf"
    inspect_gguf(path)
