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
**Status**: Stable
**Environment**: RTX 5060 Ti (16GB), PyTorch 2.6+, CUDA 12+
