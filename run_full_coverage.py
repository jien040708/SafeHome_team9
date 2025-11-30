"""
전체 프로젝트 Coverage 측정 스크립트

이 스크립트는 프로젝트의 전체 coverage를 측정하고 리포트를 생성합니다.
"""

import sys
import subprocess
from pathlib import Path


def run_full_coverage(
    output_format='html',
    fail_under=68,
    source_dirs=None,
    exclude_patterns=None
):
    """
    전체 프로젝트 coverage를 측정합니다.
    
    Args:
        output_format: 리포트 포맷 ('html', 'term', 'xml', 'json' 등)
        fail_under: 최소 coverage 퍼센트 (이보다 낮으면 실패)
        source_dirs: 측정할 소스 디렉토리 리스트 (None이면 전체)
        exclude_patterns: 제외할 패턴 리스트
    """
    
    # 기본 소스 디렉토리
    if source_dirs is None:
        source_dirs = [
            'security',
            'domain',
            'config',
            'auth',
            'storage',
            'surveillance',
            'devices',
            'event_logging',
        ]
    
    # 제외할 패턴
    if exclude_patterns is None:
        exclude_patterns = [
            '*/tests/*',
            '*/test_*.py',
            '*/__pycache__/*',
            '*/virtual_device*/*',
        ]
    
    # pytest 명령어 구성
    cmd = ['pytest']
    
    # Coverage 옵션 추가
    cmd.append('--cov')
    for src_dir in source_dirs:
        cmd.append(f'--cov={src_dir}')
    
    # 제외 패턴 추가
    for pattern in exclude_patterns:
        cmd.append(f'--cov-config=.coveragerc' if Path('.coveragerc').exists() else '')
    
    # 리포트 포맷
    report_formats = output_format.split(',') if ',' in output_format else [output_format]
    for fmt in report_formats:
        if fmt == 'html':
            cmd.append('--cov-report=html:htmlcov')
        elif fmt == 'term':
            cmd.append('--cov-report=term-missing')
        elif fmt == 'xml':
            cmd.append('--cov-report=xml')
        elif fmt == 'json':
            cmd.append('--cov-report=json:coverage.json')
    
    # 최소 coverage 설정
    if fail_under:
        cmd.append(f'--cov-fail-under={fail_under}')
    
    # 테스트 파일 찾기
    test_dirs = [
        'tests',
        'security',  # security/test_security_system.py
    ]
    
    test_patterns = []
    for test_dir in test_dirs:
        test_path = Path(test_dir)
        if test_path.exists():
            if test_path.is_dir():
                test_patterns.append(f'{test_dir}/**/test_*.py')
            elif test_path.suffix == '.py':
                test_patterns.append(str(test_path))
    
    # 테스트 파일이 있으면 추가
    if test_patterns:
        for pattern in test_patterns:
            cmd.append(pattern)
    else:
        cmd.append('tests/')
        if Path('security/test_security_system.py').exists():
            cmd.append('security/test_security_system.py')
    
    # verbose 모드
    cmd.append('-v')
    
    print("=" * 70)
    print("전체 프로젝트 Coverage 측정 시작")
    print("=" * 70)
    print(f"소스 디렉토리: {', '.join(source_dirs)}")
    print(f"출력 포맷: {output_format}")
    print(f"최소 Coverage: {fail_under}%")
    print(f"\n실행 명령어: {' '.join(cmd)}")
    print("=" * 70)
    print()
    
    # 명령어 실행
    try:
        result = subprocess.run(cmd, check=False)
        
        print()
        print("=" * 70)
        if result.returncode == 0:
            print("✅ Coverage 측정 완료!")
            print(f"\n📊 HTML 리포트: htmlcov/index.html")
            if 'json' in report_formats:
                print(f"📊 JSON 리포트: coverage.json")
            if 'xml' in report_formats:
                print(f"📊 XML 리포트: coverage.xml")
        else:
            print("⚠️ Coverage 측정 완료 (일부 실패 또는 목표 미달)")
            print(f"\n상세 내용은 위의 출력을 확인하세요.")
        print("=" * 70)
        
        return result.returncode == 0
        
    except FileNotFoundError:
        print("❌ 오류: pytest가 설치되어 있지 않습니다.")
        print("다음 명령어로 설치하세요: pip install pytest pytest-cov")
        return False
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False


def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='전체 프로젝트 Coverage 측정'
    )
    parser.add_argument(
        '--format',
        default='html,term',
        help='리포트 포맷 (html,term,xml,json - 콤마로 구분)'
    )
    parser.add_argument(
        '--fail-under',
        type=int,
        default=68,
        help='최소 coverage 퍼센트 (기본: 68)'
    )
    parser.add_argument(
        '--src',
        nargs='+',
        help='측정할 소스 디렉토리 (기본: 모든 주요 디렉토리)'
    )
    
    args = parser.parse_args()
    
    success = run_full_coverage(
        output_format=args.format,
        fail_under=args.fail_under,
        source_dirs=args.src
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

