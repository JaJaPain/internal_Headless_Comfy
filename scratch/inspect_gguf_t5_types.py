import gguf
import sys

def inspect_gguf_t5(path):
    try:
        reader = gguf.GGUFReader(path)
        for tensor in reader.tensors:
            if "attn_rel_b" in tensor.name or "token_embd" in tensor.name or "output_norm" in tensor.name:
                print(f"Tensor: {tensor.name}, Type: {tensor.tensor_type}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    path = "ComfyUI_Backend/models/text_encoders/t5-v1_1-xxl-encoder-Q5_K_M.gguf"
    inspect_gguf_t5(path)
