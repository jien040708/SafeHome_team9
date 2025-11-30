"""
빠른 Coverage 측정 스크립트 (특정 모듈만)

특정 모듈이나 파일의 coverage만 빠르게 측정할 수 있습니다.
"""

import sys
import subprocess
from pathlib import Path


def run_quick_coverage(module_or_file, output_format='term'):
    """
    특정 모듈이나 파일의 coverage를 빠르게 측정합니다.
    
    Args:
        module_or_file: 측정할 모듈 또는 파일 경로
                       예: 'security.security_system', 'security/security_system.py'
        output_format: 리포트 포맷 ('term', 'html', 'json' 등)
    """
    
    # 모듈 경로로 변환
    if module_or_file.endswith('.py'):
        # 파일 경로를 모듈 경로로 변환
        module_path = module_or_file.replace('/', '.').replace('\\', '.').replace('.py', '')
    else:
        module_path = module_or_file
    
    # 관련 테스트 파일 찾기
    test_files = []
    
    # 테스트 디렉토리에서 찾기
    test_patterns = [
        f'tests/**/test_*{Path(module_or_file).stem}*.py',
        f'tests/**/test_*{module_path.split(".")[-1]}*.py',
        f'**/test_{Path(module_or_file).stem}.py',
        f'{Path(module_or_file).parent}/test_{Path(module_or_file).stem}.py',
    ]
    
    for pattern in test_patterns:
        for test_file in Path('.').glob(pattern):
            if test_file.exists():
                test_files.append(str(test_file))
    
    # 기본 테스트 디렉토리 전체 포함
    if not test_files:
        test_files.append('tests/')
        # security 디렉토리의 테스트 파일도 포함
        if Path('security/test_security_system.py').exists():
            test_files.append('security/test_security_system.py')
    
    # pytest 명령어 구성
    cmd = [
        'pytest',
        '-v',
        f'--cov={module_path}',
    ]
    
    # 리포트 포맷
    if output_format == 'html':
        cmd.append('--cov-report=html:htmlcov')
    elif output_format == 'term':
        cmd.append('--cov-report=term-missing')
    elif output_format == 'json':
        cmd.append('--cov-report=json')
    
    # 테스트 파일 추가
    cmd.extend(test_files)
    
    print("=" * 70)
    print(f"빠른 Coverage 측정: {module_or_file}")
    print("=" * 70)
    print(f"모듈 경로: {module_path}")
    print(f"테스트 파일: {', '.join(test_files) if test_files else '자동 검색'}")
    print(f"\n실행 명령어: {' '.join(cmd)}")
    print("=" * 70)
    print()
    
    # 명령어 실행
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode == 0
    except FileNotFoundError:
        print("❌ 오류: pytest가 설치되어 있지 않습니다.")
        return False
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False


def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='빠른 Coverage 측정 (특정 모듈만)'
    )
    parser.add_argument(
        'module',
        help='측정할 모듈 또는 파일 (예: security.security_system 또는 security/security_system.py)'
    )
    parser.add_argument(
        '--format',
        default='term',
        choices=['term', 'html', 'json'],
        help='리포트 포맷 (기본: term)'
    )
    
    args = parser.parse_args()
    
    success = run_quick_coverage(args.module, args.format)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

