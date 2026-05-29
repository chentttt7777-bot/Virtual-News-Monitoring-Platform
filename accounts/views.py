from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import UserHistory

# 注册视图
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 自动登录用户
            return redirect('index')  # 重定向到主页
        # 表单验证失败时
        errors = []
        for field, error_list in form.errors.items():
            errors.extend(error_list)
        request.session['register_error'] = "注册失败: " + ", ".join(errors)

    # 无论是GET还是POST失败都重定向到首页
    return redirect('index')

# 登录视图
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            # 将错误信息存储在session中
            request.session['login_error'] = "用户名或密码错误"
    return redirect('index')

# 注销视图
@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

#清除错误信息的视图
def clear_login_error(request):
    if 'login_error' in request.session:
        del request.session['login_error']
    return JsonResponse({'status': 'ok'})

def clear_register_error(request):
    if 'register_error' in request.session:
        del request.session['register_error']
    return JsonResponse({'status': 'ok'})


@login_required
@require_http_methods(["POST"])
def save_history(request):
    UserHistory.objects.create(
        user=request.user,
        content=request.POST.get('content', '')
    )
    return JsonResponse({'status': 'success'})


@login_required
@require_http_methods(["GET"])
def get_history(request):
    histories = UserHistory.objects.filter(user=request.user).order_by('-id')[:20]  # 使用ID排序
    data = [{'content': h.content} for h in histories]
    return JsonResponse({'history': data})


@login_required
@require_http_methods(["POST"])
def clear_history(request):
    try:
        # 删除当前用户的所有历史记录
        UserHistory.objects.filter(user=request.user).delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        # 捕获异常并返回错误信息
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)