"""
pytest configuration and shared fixtures for surveillance tests
"""
import pytest
import sys
from pathlib import Path

from utils.constants import VIRTUAL_DEVICE_DIR

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def project_root_path():
    """프로젝트 루트 경로 반환"""
    return Path(__file__).parent.parent.parent


@pytest.fixture
def sample_camera_images_dir(project_root_path):
    """샘플 카메라 이미지 디렉토리 경로"""
    return project_root_path / VIRTUAL_DEVICE_DIR
