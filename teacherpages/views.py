from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import logout
from .models import GroupsTable, SubgroupsTable, AuthUser, StudentsTable, AttendanceTable, WeeksTable
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from webway.decorators import group_required
from datetime import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse

@login_required
@group_required('teacher')
def index(request):
    current_teacher  = AuthUser.objects.get(username = request.user)
    groups = GroupsTable.objects.all()
    patronymic = current_teacher.patronymic if current_teacher.patronymic else ''
    return render(request, 'teacherpages/startpage.html', {'groups': groups, 'name': current_teacher.first_name, 'patronymic': patronymic})

@login_required
@group_required('teacher')
def subgroups_select(request, key_group):
    subgroups = SubgroupsTable.objects.filter(key_group=key_group)
    group = GroupsTable.objects.get(id_groups_table=key_group)
    return render(request, 'teacherpages/subgroups_select.html', {'subgroups': subgroups, 'group': group})

@login_required
@group_required('teacher')
def table_students(request, key_subgroup):
    students = StudentsTable.objects.filter(key_subgroup=key_subgroup).order_by('student_name')
    subgroup = SubgroupsTable.objects.get(id_subgroups_table=key_subgroup)
    weeks = WeeksTable.objects.all().order_by('id_weeks_table')
    attendance_data = []
    for student in students:
            student_attendance = {}
            attendance_records = AttendanceTable.objects.filter(id_student=student.id_students_table)
            for week in weeks:
                student_attendance[week.id_weeks_table] = {'attendance_disrespectfully': None,'attendance_respectfully': None,'comment': ''}
            for record in attendance_records:
                student_attendance[record.id_week.id_weeks_table].update({'attendance_disrespectfully': record.attendance_disrespectfully,'attendance_respectfully': record.attendance_respectfully})
            attendance_data.append({'student': student, 'attendance': student_attendance})
    month_data = []
    prev_month = None
    month_span = 0
    for week in weeks:
        start_date_str, end_date_str = week.week_name.split(' - ')
        start_date = datetime.strptime(start_date_str, '%d.%m')
        month_name = {
            1: 'Январь',
            2: 'Февраль',
            3: 'Март',
            4: 'Апрель',
            5: 'Май',
            6: 'Июнь',
            7: 'Июль',
            8: 'Август',
            9: 'Сентябрь',
            10: 'Октябрь',
            11: 'Ноябрь',
            12: 'Декабрь'
        }[start_date.month]

        if month_name != prev_month:
            if prev_month is not None:
                month_data.append({
                    'month_name': prev_month,
                    'month_span': 2 * month_span
                })
            month_span = 0
            prev_month = month_name

        month_span += 1

    if prev_month is not None:
        month_data.append({
            'month_name': prev_month,
            'month_span': 2 * month_span
        })
    return render(request, 'teacherpages/table_students.html', {'attendance_data': attendance_data, 'subgroup': subgroup, 'weeks': weeks, 'month_data': month_data})

@login_required
@group_required('teacher')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
@group_required('teacher')
def options(request):
    user = AuthUser.objects.get(username = request.user)
    return render(request, 'teacherpages/options.html', {'user': user})

@login_required
@group_required('teacher')
def update_account(request):
    if request.method == 'POST':
        
        user = AuthUser.objects.get(username = request.user)
        current_password = request.POST.get('current_password')
        if not check_password(current_password, user.password):
            return render(request, 'teacherpages/options.html', {'message': 'Неверный текущий пароль'})
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        mail = request.POST.get('mail')
        patronymic = request.POST.get('patronymic')

        print(patronymic, user.patronymic)
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
        return render(request, 'teacherpages/options.html', {'message': 'Данные аккаунта успешно обновлены!'})

    return render(request, 'teacherpages/options.html')

@login_required
@group_required('teacher')
def search_students_teacher(request):
    if request.method == 'POST':
        searchName = request.POST.get('SearchStudentName')
        searchCol = int(request.POST.get('SearchAttendance'))
        result = []
        if searchName:
            searchStudents = StudentsTable.objects.filter(Q(student_name__icontains=searchName))
        else:
            searchStudents = StudentsTable.objects.all()
        for student in searchStudents:     
            searchAttendances = AttendanceTable.objects.filter(id_student = student.id_students_table)
            sumAttendance = 0
            for attendance in searchAttendances:
                sumAttendance += (attendance.attendance_respectfully or 0) + (attendance.attendance_disrespectfully or 0)
            if sumAttendance >= searchCol:
                result.append({'subgroupName': student.key_subgroup.subgroup_name, 'subgroupId': reverse('table_students_teacher', args=[student.key_subgroup.id_subgroups_table]), 'name': student.student_name, 'attendances': sumAttendance})
        print(result)
        return JsonResponse({'success': True, 'result': result})
    else:
        return JsonResponse({'success': False, 'message': 'Метод запроса не поддерживается'})