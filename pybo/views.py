import json
import pandas as pd
from django.conf import settings
from django.shortcuts import render


def dashboard(request):
    # 1. CSV 파일 경로 설정
    summary_path = settings.BASE_DIR / 'DATA' / 'summary.csv'
    dau_path = settings.BASE_DIR / 'DATA' / 'dau.csv'
    test_data_path = settings.BASE_DIR / 'DATA' / 'test-data.csv'

    try:
        # 2. CSV 파일에서 데이터 읽기
        # 요약 데이터 (카드)
        summary_df = pd.read_csv(summary_path)
        summary_data = summary_df.set_index('Metric')['Value'].to_dict()

        # 차트 데이터
        dau_df = pd.read_csv(dau_path)
        chart_labels = dau_df['Date'].tolist()
        chart_data = dau_df['Users'].tolist()

        # 최근 가입자 데이터 읽기 (헤더가 없으므로 names로 컬럼명 지정)
        recent_users_df = pd.read_csv(test_data_path, header=None, names=['name', 'nickname'])
        recent_users = recent_users_df.to_dict('records')

    except FileNotFoundError:
        # 파일이 없을 경우를 대비한 기본값
        summary_data = {key: 0 for key in ['total_users', 'mau', 'total_posts', 'total_likes', 'total_comments', 'total_bookmarks', 'total_notifications']}
        chart_labels = ['데이터 없음']
        chart_data = [0]
        recent_users = []

    context = {
        'summary': summary_data,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'recent_users': recent_users,
    }
    return render(request, 'pybo/test.html', context)