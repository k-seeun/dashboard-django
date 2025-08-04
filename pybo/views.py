import json
import pandas as pd
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment, Post
from .forms import CommentForm
from django.http import JsonResponse
from .forms import PostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate

def dashboard(request):
    summary_path = settings.BASE_DIR / 'DATA' / 'summary.csv'
    test_data_path = settings.BASE_DIR / 'DATA' / 'test-data.csv'

    try:
        summary_df = pd.read_csv(summary_path)

        # DB에서 최신 데이터 가져오기
        total_users_db = User.objects.count()
        total_comments_db = Comment.objects.count()
        total_posts_db = Post.objects.count()
        total_likes_db = Post.objects.aggregate(total_likes=Sum('like_count'))['total_likes'] or 0

        # DataFrame의 값 업데이트
        summary_df.loc[summary_df['Metric'] == 'total_users', 'Value'] = total_users_db
        summary_df.loc[summary_df['Metric'] == 'total_comments', 'Value'] = total_comments_db
        summary_df.loc[summary_df['Metric'] == 'total_posts', 'Value'] = total_posts_db
        summary_df.loc[summary_df['Metric'] == 'total_likes', 'Value'] = total_likes_db

        # 변경된 DataFrame을 다시 CSV 파일에 저장
        summary_df.to_csv(summary_path, index=False)

        # 템플릿에 전달할 데이터 준비 (업데이트된 DataFrame 사용)
        summary_data = summary_df.set_index('Metric')['Value'].to_dict()

        # 일별 게시글 수를 계산하여 차트 데이터로 사용
        daily_posts = (
            Post.objects.annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

        chart_labels = [item['date'].strftime('%Y-%m-%d') for item in daily_posts]
        chart_data = [item['count'] for item in daily_posts]

        recent_users_df = pd.read_csv(test_data_path, header=None, names=['name', 'nickname'])
        recent_users = recent_users_df.to_dict('records')

    except FileNotFoundError:
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

def comment_create_view(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pybo:comment_create') # 성공 시 새로고침
    else:
        form = CommentForm()

    comments = Comment.objects.order_by('-created_at')  # 최신 댓글부터 보여줌
    return render(request, 'pybo/comment_form.html', {'form': form, 'comments': comments})

def like_comment(request, comment_id):
    if request.method == "POST":
        # 객체가 없을 때 404 오류를 반환하도록 get_object_or_404 사용
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.like_count += 1
        comment.save()
        return JsonResponse({'like_count': comment.like_count})

def comment_delete_view(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.delete()
    return redirect('pybo:comment_create')

def post_create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            # 게시글 등록 후, 같은 페이지로 리디렉션하여 목록을 바로 확인
            return redirect('pybo:post_create')
    else:
        form = PostForm()

    # 등록된 모든 게시글을 최신순으로 가져옴
    posts = Post.objects.order_by('-created_at')
    context = {'form': form, 'posts': posts}
    return render(request, 'pybo/post_form.html', context)

def post_like(request, post_id):
    """
    pybo 게시글 좋아요 (AJAX 처리)
    """
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        post.like_count += 1
        post.save()
        return JsonResponse({'like_count': post.like_count})
    # POST 요청이 아닐 경우 에러 응답
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def post_delete(request, post_id):
    """
    pybo 게시글삭제
    """
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        post.delete()

    return redirect('pybo:post_create')
