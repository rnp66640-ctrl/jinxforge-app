# TripoSR install notes — CPU-only recipe proven on the shop VM (2026-10-30)

The plain `pip install -r requirements.txt` does NOT work out of the box on Python 3.12.
The proven recipe (this VM: no GPU, Python 3.12.3):

1. Pin PyTorch for CPU: torch==2.3.1+cpu and torchvision==0.18.1+cpu from the PyTorch CPU index.
2. torchmcubes (a git dependency) refuses build isolation: install scikit-build-core, cmake,
   ninja, and pybind11 into the venv first, then build it against the installed torch.
3. transformers==4.35.0 pins huggingface-hub<0.18 through tokenizers; pin huggingface-hub==0.16.4.
4. onnxruntime is not pulled in automatically but rembg needs it; install it separately.

Facts from the run:
- Weights are public: stabilityai/TripoSR on Hugging Face, no login or token. model.ckpt is 1.68 GB.
- run.py detects a missing CUDA device and falls back to CPU by itself. Default output is OBJ
  with vertex colours; rendering is opt-in (--render) and off by default.
- The README states the default options take about 6 GB VRAM for one image. Richard's laptop
  card is 6 GB: exactly at the line. --chunk-size (default 8192) is the documented lever that
  lowers memory at the cost of speed.
