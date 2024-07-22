import logging
import torch

logger = logging.getLogger(__name__)


# Set torch device
def get_torch_device() -> str:
    logger.debug(f"PyTorch version: {torch.__version__}")

    # Set the device
    if torch.cuda.is_available():
        device = 'cuda'
    elif torch.backends.mps.is_available():
        device = 'mps'
    else:
        device = 'cpu'
    logger.debug(f"Using device: {device}")
    return device
