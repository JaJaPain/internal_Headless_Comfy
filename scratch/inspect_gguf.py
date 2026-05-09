import gguf
import sys

def inspect_gguf(path):
    try:
        reader = gguf.GGUFReader(path)
        print(f"Inspecting GGUF: {path}")
        print(f"Tensor count: {len(reader.tensors)}")
        for i, tensor in enumerate(reader.tensors):
            # Print if it doesn't start with enc.blk. or if it's the first/last of a block
            if not tensor.name.startswith("enc.blk."):
                print(f"Tensor {i}: {tensor.name}")
            elif ".0." in tensor.name or f".{len(reader.tensors)//9-1}." in tensor.name:
                 print(f"Tensor {i}: {tensor.name}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    path = "ComfyUI_Backend/models/text_encoders/t5-v1_1-xxl-encoder-Q5_K_M.gguf"
    inspect_gguf(path)
