# config.py

# 설정 가능한 변수들
NUM_EMPLOYEES = 1000    # 직원 수
NUM_CUSTOMERS = 225000   # 고객 수
MIN_CONTRACTS_PER_CUSTOMER = 1  # 고객당 최소 계약 수
MAX_CONTRACTS_PER_CUSTOMER = 2  # 고객당 최대 계약 수

# 파일 경로 설정
NAMES_FILE_PATH = '/Users/mac/Documents/study/python/이름데이터.xlsx'
PRODUCTS_FILE_PATH = 'gen_fake_data/2409_보람상조/products_input.csv'

# 필드 값 비율 설정
FIELD_DISTRIBUTIONS = {
    'employee_positions': {
        '사원': 0.5,
        '주임': 0.2,
        '대리': 0.15,
        '과장': 0.1,
        '차장': 0.04,
        '부장': 0.01
    },
    'employee_branches': {
        # 지점별 비율 설정 (예시로 서울특별시의 비율을 높게 설정)
        '서울특별시': 0.3,
        '부산광역시': 0.1,
        '대구광역시': 0.1,
        '인천광역시': 0.1,
        '광주광역시': 0.2,
        '대전광역시': 0.1,
        '울산광역시': 0.05,
        '세종특별자치시': 0.02,
        '경기도': 0.5,
        '강원도': 0.2,
        '충청북도': 0.3,
        '충청남도': 0.4,
        '전라북도': 0.2,
        '전라남도': 0.2,
        '경상북도': 0.01,
        '경상남도': 0.12,
        '제주특별자치도' : 0.1
    },
    'contract_statuses': {
        '진행중': 0.7,
        '완료': 0.25,
        '해지': 0.05
    },
    'collection_methods': {
        '자동이체': 0.6,
        '카드결제': 0.3,
        '현금': 0.1
    },
    'collection_statuses': {
        '완료': 0.0,
        '연체': 0.0,
        '미납': 0.0
    },
    # 추가적으로 필드별 비율 설정 가능
}

# 계약 해지 사유 설정
TERMINATION_REASONS = {
    '서비스 불만족': 0.41,
    '경제적 어려움': 0.32,
    '타사로 변경': 0.15,
    '사용 필요성 감소': 0.14,
    '기타': 0.05
}

# 계약 해지 설정
CONTRACT_TERMINATION_SETTINGS = {
    'termination_months': {
        'distribution': 'normal',  # 분포 종류: 'uniform', 'normal', 'exponential' 등
        'min_months': 1,            # 최소 개월 수
        'max_months': None,          # 최대 개월 수 (None이면 만기 예정일까지)
        'mean': 72,               # 정규 분포 사용 시 평균 (필요 시 추가)
        'stddev': 3,              # 정규 분포 사용 시 표준편차 (필요 시 추가)
        'lambda': 0.2             # 지수 분포 사용 시 람다 값 (필요 시 추가)
    }
}

# 이상치 설정
OUTLIER_SETTINGS = {
    # 'employee_salary' 관련 설정 제거
    # 다른 필드에 대한 이상치 설정 가능
}