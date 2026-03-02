import random
from django.contrib.auth.models import User
from core.models import Case, Comment, Follow

def run():
    print("--- เริ่มการสร้างข้อมูล Mock Data ---")

    # 1. สร้าง Users (5 นักศึกษา และ 5 เจ้าหน้าที่)
    roles = ['student', 'staff']
    users = []
    
    for role in roles:
        for i in range(1, 6):
            username = f"{role}_{i}"
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    password='password123',
                    email=f"{username}@ubu.ac.th",
                    is_staff=(role == 'staff')
                )
                users.append(user)
                print(f"สร้าง User: {username}")
            else:
                users.append(User.objects.get(username=username))

    # 2. รายการข้อมูลตัวอย่างสำหรับ Case
    titles = [
        "หลอดไฟทางเดินหอพัก 7 เสีย", "ท่อน้ำประปาแตกหน้าคณะวิศวฯ", 
        "ฝาท่อระบายน้ำชำรุดบริเวณโรงอาหารกลาง", "ปลั๊กไฟในห้องสมุดใช้งานไม่ได้",
        "หญ้ายาวเกินไปบริเวณสนามฟุตบอล", "เครื่องปรับอากาศห้องเรียน SC-302 ไม่เย็น",
        "พบขยะสะสมบริเวณประตูทางเข้ามหาวิทยาลัย", "กล้องวงจรปิดหน้าอาคารสำนักงานอธิการบดีดับ"
    ]
    
    descriptions = [
        "แจ้งซ่อมด่วนครับ มืดมากตอนกลางคืน เสี่ยงอันตราย", 
        "น้ำไหลนองเต็มถนนมา 2 วันแล้วครับ", 
        "เกรงว่านักศึกษาจะเดินตกท่อครับ รบกวนตรวจสอบด้วย", 
        "ลองเสียบแล้วไม่มีไฟเข้าเลยครับ ทั้งแถวเลย",
        "บดบังทัศนียภาพและอาจเป็นที่อยู่ของสัตว์มีพิษ", 
        "แอร์มีแต่ลมออกมาครับ รบกวนช่างเข้ามาดูหน่อยครับ"
    ]

    categories = ['electrical', 'water_supply', 'road_damage', 'other']
    statuses = ['pending', 'in_progress', 'resolved']

    # 3. สร้าง Case (เรื่องร้องเรียน) จำนวน 15 เรื่อง
    all_cases = []
    reporters = [u for u in users if not u.is_staff] # นักศึกษาเป็นคนแจ้ง
    
    for i in range(15):
        case = Case.objects.create(
            title=random.choice(titles) + f" (เคสที่ {i+1})",
            description=random.choice(descriptions),
            category=random.choice(categories),
            status=random.choice(statuses),
            reporter=random.choice(reporters)
        )
        all_cases.append(case)
        print(f"สร้าง Case: {case.title} [สถานะ: {case.get_status_display()}]")

    # 4. สร้างการติดตาม (Follow)
    for user in users:
        # สุ่มให้แต่ละคนติดตาม 3 เคส
        followed_cases = random.sample(all_cases, 3)
        for case in followed_cases:
            Follow.objects.get_or_create(user=user, case=case)
        print(f"User: {user.username} เริ่มติดตามเคสบางส่วนแล้ว")

    # 5. สร้างความคิดเห็น (Comments)
    comment_texts = [
        "รับทราบครับ กำลังประสานงานช่างให้",
        "ดำเนินการแก้ไขให้เรียบร้อยแล้วนะครับ",
        "ขอบคุณที่แจ้งเข้ามาครับ จะรีบเข้าไปดูให้ด่วนที่สุด",
        "ตอนนี้รออะไหล่อยู่ครับ คาดว่าจะเสร็จพรุ่งนี้",
        "จุดนี้เป็นความรับผิดชอบของเทศบาล กำลังประสานงานต่อให้ครับ"
    ]

    for case in all_cases:
        # สุ่มให้แต่ละเคสมี 1-3 คอมเมนต์
        num_comments = random.randint(1, 3)
        for _ in range(num_comments):
            Comment.objects.create(
                case=case,
                author=random.choice(users),
                content=random.choice(comment_texts)
            )
    
    print(f"สร้าง Comments เรียบร้อยสำหรับทุกเคส")
    print("--- สำเร็จ! ข้อมูล Mock Data พร้อมใช้งานแล้ว ---")
    print("หมายเหตุ: รหัสผ่านของทุก User คือ 'password123'")