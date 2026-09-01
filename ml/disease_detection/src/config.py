from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Dataset
DATASET_DIR = (
    PROJECT_ROOT
    / "dataset"
    / "archive"
    / "PlantVillage"
)

# Model output directory
MODEL_DIR = PROJECT_ROOT / "models"

# Image configuration
IMAGE_SIZE = (224, 224)

# Training configuration
BATCH_SIZE = 32
RANDOM_SEED = 42

# Dataset split
VALIDATION_SPLIT = 0.20
TEST_SPLIT = 0.10