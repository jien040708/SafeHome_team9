"""
테스트용 유틸리티 함수들
"""
from unittest.mock import MagicMock


def create_mock_row(data: dict):
    """
    sqlite3.Row를 모방하는 Mock 객체 생성
    dict()로 변환 가능하고, 딕셔너리처럼 접근 가능
    
    Args:
        data: Row 데이터 딕셔너리
        
    Returns:
        딕셔너리처럼 접근 가능한 객체 (dict()로 변환 가능)
    """
    # dict()로 변환 가능한 객체 생성 (dict 상속)
    return dict(data)

