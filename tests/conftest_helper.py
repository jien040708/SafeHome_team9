"""
테스트용 헬퍼 함수들
"""
from unittest.mock import Mock
from typing import Any, Dict, List, Optional


def create_mock_row(data: Dict[str, Any]) -> Mock:
    """
    sqlite3.Row를 모방하는 Mock 객체 생성
    
    Args:
        data: Row 데이터 딕셔너리
        
    Returns:
        딕셔너리처럼 접근 가능한 Mock 객체
    """
    mock_row = Mock()
    
    # 딕셔너리처럼 접근 가능하도록 설정
    def getitem(key):
        return data[key]
    
    def contains(key):
        return key in data
    
    mock_row.__getitem__ = Mock(side_effect=getitem)
    mock_row.__contains__ = Mock(side_effect=contains)
    
    # 속성 접근도 지원
    for key, value in data.items():
        setattr(mock_row, key, value)
        # 딕셔너리 접근 방식도 지원
        type(mock_row).__getitem__ = Mock(side_effect=lambda self, k: data[k])
    
    return mock_row


def create_mock_rows(data_list: List[Dict[str, Any]]) -> List[Mock]:
    """
    여러 sqlite3.Row를 모방하는 Mock 객체 리스트 생성
    
    Args:
        data_list: Row 데이터 딕셔너리 리스트
        
    Returns:
        Mock 객체 리스트
    """
    return [create_mock_row(data) for data in data_list]

