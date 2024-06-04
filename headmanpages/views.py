from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import logout
from .models import StudentsTable, AuthUser, AttendanceTable, SubgroupsTable, AccessWeeksTable, WeeksTable
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from webway.decorators import group_required
import json

@login_required
@group_required('headman')
def index(request):
    current_headman  = AuthUser.objects.get(username = request.user)
    subgroup_key = current_headman.key_subgroups
    patronymic = current_headman.patronymic if current_headman.patronymic else ''
    groupmates = StudentsTable.objects.filter(key_subgroup = subgroup_key).order_by('student_name')
    weeks_access = AccessWeeksTable.objects.filter(subgroup = subgroup_key.id_subgroups_table).values('week')
    weeks = []
    for item in weeks_access:
        week = item['week']
        weeks.append(WeeksTable.objects.get(id_weeks_table = week))
    #weeks = WeeksTable.objects.filter(id_weeks_table = weeks_access).order_by('week')
    return render(request, 'headmanpages/startpage.html', {'subgroup_key': subgroup_key, 'groupmates': groupmates, 'weeks': weeks, 'name': current_headman.first_name, 'patronymic': patronymic})

@login_required
@group_required('headman')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
@group_required('headman')
def save_attendance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.POST['data'])  # Преобразуем строку JSON в список словарей
            week = data[0]['week_id']
            for item in data:
                id_student = item['student_id']
                respectfully = item['respectfully']
                disrespectfully = item['disrespectfully']
                if (respectfully == 0):
                    respectfully = None
                if (disrespectfully == 0):
                    disrespectfully = None
                if (respectfully == disrespectfully == None):
                    AttendanceTable.objects.filter(id_student_id=id_student, id_week_id=week).delete()
                else:
                    attendance = AttendanceTable.objects.filter(id_student=id_student, id_week=week).first()
                    if attendance:
                        AttendanceTable.objects.filter(id_student=id_student, id_week=week).update(attendance_respectfully=None,attendance_disrespectfully=(disrespectfully or 0) + (respectfully or 0))
                    else:
                        attendance = AttendanceTable.objects.create(
                            id_student_id=id_student,
                            id_week_id=week,
                            attendance_respectfully= None,
                            attendance_disrespectfully = (disrespectfully or 0) + (respectfully or 0)
                        )
            st = data[0]['student_id']
            student_for_subgroups_search = StudentsTable.objects.filter(id_students_table = st).first()
            existing_record = AccessWeeksTable.objects.filter(week=week, subgroup=student_for_subgroups_search.key_subgroup).update(color_sent = 'Y')

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Метод запроса не поддерживается'})

@login_required
@group_required('headman')
def add_student(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        key_subgroup_id = request.POST.get('key_subgroup')  # Получаем ID подгруппы
        key_subgroup = get_object_or_404(SubgroupsTable, id_subgroups_table=key_subgroup_id)  # Получаем объект SubgroupsTable по ID
        searchStudent = StudentsTable.objects.filter(student_name=student_name, key_subgroup=key_subgroup).first()
        try:
            if searchStudent:
                raise Exception("Студент с таким именем уже есть в данной группе!")
            new_student = StudentsTable.objects.create(student_name=student_name, key_subgroup=key_subgroup)
            success = True
            message = "Студент успешно добавлен!"
        except Exception as e:
            success = False
            message = str(e)
        
        return JsonResponse({'success': success, 'message': message})
    else:
        return JsonResponse({'success': False, 'message': 'Метод запроса не поддерживается'})
    
@login_required
@group_required('headman')
def del_student(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        key_subgroup_id = request.POST.get('key_subgroup')  # Получаем ID подгруппы
        key_subgroup = get_object_or_404(SubgroupsTable, id_subgroups_table=key_subgroup_id)  # Получаем объект SubgroupsTable по ID
        try:
            student = StudentsTable.objects.get(student_name=student_name, key_subgroup=key_subgroup)
            student.delete()
            success = True
            message = "Студент успешно отчислен!"
        except Exception as e:
            success = False
            message = str(e)
        
        return JsonResponse({'success': success, 'message': message})
    else:
        return JsonResponse({'success': False, 'message': 'Метод запроса не поддерживается'})

@login_required
@group_required('headman')
def options(request):
    user = AuthUser.objects.get(username = request.user)
    return render(request, 'headmanpages/options.html', {'user': user})

@login_required
@group_required('headman')
def update_account(request):
    if request.method == 'POST':
        
        user = AuthUser.objects.get(username = request.user)
        current_password = request.POST.get('current_password')
        if not check_password(current_password, user.password):
            return render(request, 'headmanpages/options.html', {'message': 'Неверный текущий пароль'})
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        mail = request.POST.get('mail')
        patronymic = request.POST.get('patronymic')

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if patronymic:
            user.patronymic = patronymic
        if mail:
            user.email = mail
        if password:
            hashed_password = make_password(password)
            user.password = hashed_password
        
        user.save()
        return render(request, 'headmanpages/options.html', {'message': 'Данные аккаунта успешно обновлены!'})

    return render(request, 'headmanpages/options.html')