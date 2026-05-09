# WanVideo GGUF Pipeline: Implementation & Troubleshooting Guide

This document outlines the critical issues encountered and resolved during the stabilization of the WanVideo GGUF pipeline on the Blackwell (RTX 50) architecture.

## 1. T5 Text Encoder: GGUF Key Mapping
**Problem**: The GGUF version of the T5-XXL encoder uses a naming convention (`enc.blk.X`) that deviates from the standard HuggingFace structure expected by the WanVideo wrapper.
**Solution**: Modified `nodes_model_loading.py` to include a robust mapping layer that translates GGUF block names and normalization layers (e.g., `attn_norm` -> `norm1`) into the model's internal hierarchy.

## 2. Vocabulary Mismatch (GGUF vs. Tokenizer)
**Problem**: Most GGUF T5 models are exported with a 32,128-token vocabulary (T5-v1.1 standard). However, the WanVideo tokenizer config is set for MT5 (256,384 tokens). This mismatch causes a fatal CUDA "out of bounds" index crash when the tokenizer produces an ID > 32k.
**Solution**: 
- Reverted the model to expect a 256,384 vocabulary.
- Implemented a "Dequantize & Pad" logic in the loader. The 32k GGUF token embedding is dequantized to full precision and then padded with zeros to reach the 256k required size.

## 3. Shared Relative Position Bias
**Problem**: GGUF T5 models often share relative position embeddings across layers, but the initial wrapper implementation expected per-layer embeddings.
**Solution**: Patched `wanvideo/modules/t5.py` to support the `shared_pos=True` flag and correctly map the `enc.blk.0.attn_rel_b.weight` key from GGUF to the shared position embedding layer.

## 4. CUDA Driver / PyTorch Robustness
**Problem**: Fatal "Aborted" signals occurred during positional embedding generation on Blackwell GPUs. This was traced to `torch.arange` calls directly on CUDA devices in certain PyTorch versions.
**Solution**: Modified `T5RelativeEmbedding.forward` to create the `rel_pos` tensor on the **CPU** first and then move it to the target device. This bypasses potential driver-level hook collisions.

## 5. CLIP Vision Loader Pathing
**Problem**: The custom node's CLIP loader used `get_full_path_or_raise`, which crashed the entire server if the model wasn't in the very first directory checked (`models/clip_vision`), ignoring valid fallbacks.
**Solution**: Updated the loader to use `get_full_path` and added `models/clip/` to the search sequence, ensuring the model is found regardless of standard ComfyUI folder variations.

## 6. GGUF Parameter Handling
**Problem**: Non-linear weights (like token embeddings) remained as `GGUFParameter` objects, which standard PyTorch layers cannot process, leading to crashes.
**Solution**: Added explicit dequantization for specific non-linear weight keys in the loader to ensure they are converted to standard `torch.Tensor` objects before the model starts execution.

---
## 7. API Control & The "4n + 1" Rule

To maintain stability and prevent model errors, the WanVideo 14B architecture requires that the total frame count follows the formula: **Total Frames = (4 * n) + 1**.

### Recommended Frame Counts:
- **1.0s (at 16fps)**: 17 frames
- **2.0s (at 16fps)**: 33 frames
- **3.0s (at 16fps)**: 49 frames
- **5.0s (at 16fps)**: 81 frames

### Adjusting via API:
The `server.py` accepts `num_frames` and `seed` as form data. You can adjust these in your frontend or via `test_generation.py`:

```python
data = {
    'prompt': 'Character walking loop...',
    'num_frames': 33,  # Target: 2 seconds
    'seed': 42
}
```

### Performance Trade-off:
- **13-17 frames**: ~7 mins (Fast iteration, good for pose testing)
- **33 frames**: ~18 mins (Best for basic walking cycles)
- **81 frames**: ~45 mins (Final high-fidelity production)

**Note**: If you provide a number that doesn't fit the `4n + 1` rule, the `WanVideoImageToVideoEncode` node will automatically round it down to the nearest valid integer.
