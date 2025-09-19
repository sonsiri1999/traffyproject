from tokenize import Comment
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Case, Follow, Comment ,Image
from django.contrib import messages
from django.db.models import Count
from .forms import CaseForm, CommentForm
from django.views import generic
from django.urls import reverse_lazy
def home_view(request):
    # ดึงข้อมูลเคสทั้งหมดจากฐานข้อมูล เรียงจากล่าสุดไปเก่าสุด
    all_cases = Case.objects.all().order_by('-created_at')

    # สร้าง Dictionary สำหรับเก็บจำนวนผู้ติดตามในแต่ละเคส
    case_followers = {}
    for case in all_cases:
        # นับจำนวนผู้ติดตามจากโมเดล Follow
        followers_count = Follow.objects.filter(case=case).count()
        case_followers[case.id] = followers_count

    # ส่งข้อมูลทั้งหมดไปยัง Template
    context = {
        'all_cases': all_cases,
        'case_followers': case_followers,
    }
    return render(request, 'core/home.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # ไปหน้าแรกหลังจากสมัครสำเร็จ
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    # ดึงเรื่องร้องเรียนทั้งหมดที่ผู้ใช้ปัจจุบันเป็นคนแจ้ง
    my_cases = Case.objects.filter(reporter=request.user).order_by('-created_at')
    
    # ดึงเรื่องร้องเรียนทั้งหมดที่ผู้ใช้ปัจจุบันกำลังติดตาม
    following_cases = Case.objects.filter(followers__user=request.user).order_by('-created_at')

    context = {
        'my_cases': my_cases,
        'following_cases': following_cases,
    }
    return render(request, 'core/profile.html', context)

@login_required
def create_case_view(request):
    if request.method == 'POST':
        case_form = CaseForm(request.POST, request.FILES) 
        if case_form.is_valid():
            new_case = case_form.save(commit=False)
            new_case.reporter = request.user
            new_case.save()

            # สร้างการติดตามอัตโนมัติ
            Follow.objects.create(user=request.user, case=new_case)

            return redirect('home')
    else:
        case_form = CaseForm()

    context = {
        'case_form': case_form,
    }
    return render(request, 'core/create_case.html', context)

def case_detail_view(request, case_id):
    case = get_object_or_404(Case.objects.annotate(
        follower_count=Count('followers')
    ), id=case_id)
    
    comments = case.comments.all().order_by('-created_at')

    is_following = False
    if request.user.is_authenticated:
        if Follow.objects.filter(user=request.user, case=case).exists():
            is_following = True

    if request.method == 'POST':
        if request.user.is_authenticated:
            if 'toggle_follow' in request.POST:
                if is_following:
                    Follow.objects.filter(user=request.user, case=case).delete()
                    messages.info(request, 'เลิกติดตามเรื่องนี้แล้ว')
                else:
                    Follow.objects.create(user=request.user, case=case)
                    messages.success(request, 'เริ่มติดตามเรื่องนี้แล้ว')
                return redirect('case_detail', case_id=case.id)
            
            # ใช้ CommentForm ในการจัดการการส่งฟอร์ม
            comment_form = CommentForm(request.POST, request.FILES)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.case = case
                new_comment.author = request.user
                new_comment.save()
                messages.success(request, 'เพิ่มความคิดเห็นเรียบร้อยแล้ว')
                return redirect('case_detail', case_id=case.id)
        else:
            messages.error(request, 'กรุณาเข้าสู่ระบบเพื่อดำเนินการ')
            return redirect('login')
    else:
        # สร้างฟอร์มเปล่าเพื่อส่งไปยัง Template
        comment_form = CommentForm()

    context = {
        'case': case,
        'comments': comments,
        'is_following': is_following,
        'comment_form': comment_form, # เพิ่มฟอร์มคอมเมนต์ใน context
    }
    return render(request, 'core/case_detail.html', context)

@login_required
def change_case_status(request, case_id):
    if not request.user.is_staff:
        # ถ้าผู้ใช้ไม่ใช่เจ้าหน้าที่ ให้ส่งกลับไปหน้าหลัก
        messages.error(request, 'คุณไม่มีสิทธิ์ในการเข้าถึงหน้านี้')
        return redirect('home')

    case = get_object_or_404(Case, id=case_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [status[0] for status in Case.STATUS_CHOICES]:
            case.status = new_status
            case.save()
            messages.success(request, f"เปลี่ยนสถานะเรื่อง: '{case.title}' เป็น '{case.get_status_display()}' เรียบร้อยแล้ว")
            return redirect('case_detail', case_id=case.id)

    # ส่งตัวเลือกสถานะไปยัง Template
    context = {
        'case': case,
        'status_choices': Case.STATUS_CHOICES,
    }
    return render(request, 'core/change_status.html', context)

@login_required
def staff_dashboard_view(request):
    if not request.user.is_staff:
        messages.error(request, 'คุณไม่มีสิทธิ์ในการเข้าถึงหน้านี้')
        return redirect('home')

    # กรองข้อมูลตามสถานะที่ผู้ใช้เลือก (ถ้ามี)
    status_filter = request.GET.get('status')
    if status_filter:
        all_cases = Case.objects.filter(status=status_filter).order_by('-created_at')
    else:
        all_cases = Case.objects.all().order_by('-created_at')

    # ดึงจำนวนเรื่องร้องเรียนแต่ละสถานะเพื่อแสดงในหน้าแดชบอร์ด
    case_counts = Case.objects.values('status').annotate(total=Count('status'))
    
    # แปลงข้อมูลจำนวนเคสให้อยู่ในรูปแบบที่เข้าใจง่าย
    status_counts = {item['status']: item['total'] for item in case_counts}
    
    context = {
        'all_cases': all_cases,
        'status_choices': Case.STATUS_CHOICES,
        'status_counts': status_counts,
        'selected_status': status_filter,
    }
    return render(request, 'core/staff_dashboard.html', context)

def home_view(request):
    # ดึงค่าการเรียงลำดับจาก URL ถ้าไม่มีให้เรียงตามวันที่สร้างล่าสุด
    sort_by = request.GET.get('sort', '-created_at')

    # ดึงข้อมูลเคสทั้งหมด พร้อมทั้งนับจำนวนผู้ติดตาม
    all_cases = Case.objects.annotate(
        follower_count=Count('followers')
    ).order_by(sort_by)

    context = {
        'all_cases': all_cases,
        'status_choices': Case.STATUS_CHOICES, # ส่งตัวเลือกสถานะไปด้วย
    }
    return render(request, 'core/home.html', context)

def public_dashboard_view(request):
    # ดึงข้อมูลสำหรับกราฟแท่ง (Bar Chart)
    case_status_data = Case.objects.values('status').annotate(count=Count('status')).order_by('status')
    
    status_labels = [item['status'] for item in case_status_data]
    status_counts = [item['count'] for item in case_status_data]
    readable_status_labels = [dict(Case.STATUS_CHOICES)[label] for label in status_labels]

    # ดึงข้อมูลสำหรับกราฟวงกลม (Pie Chart) - NEW
    case_category_data = Case.objects.values('category').annotate(count=Count('category')).order_by('category')
    
    category_labels = [item['category'] for item in case_category_data]
    category_counts = [item['count'] for item in case_category_data]
    readable_category_labels = [dict(Case.CATEGORY_CHOICES)[label] for label in category_labels]
    
    context = {
        'status_labels': readable_status_labels,
        'status_counts': status_counts,
        'category_labels': readable_category_labels, # เพิ่มข้อมูลหมวดหมู่
        'category_counts': category_counts, # เพิ่มข้อมูลหมวดหมู่
    }
    return render(request, 'core/public_dashboard.html', context)

class SignUpView(generic.CreateView):
    form_class = UserCreationForm  # ใช้ UserCreationForm มาตรฐานของ Django
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'