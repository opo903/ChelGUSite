# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccessWeeksTable(models.Model):
    week = models.OneToOneField('WeeksTable', models.DO_NOTHING, db_column='week', primary_key=True)  # The composite primary key (week, subgroup) found, that is not supported. The first column is selected.
    subgroup = models.ForeignKey('SubgroupsTable', models.DO_NOTHING, db_column='subgroup')
    color_sent = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'access_weeks_table'
        unique_together = (('week', 'subgroup'),)


class AttendanceTable(models.Model):
    id_student = models.OneToOneField('StudentsTable', models.DO_NOTHING, db_column='id_student', primary_key=True)
    id_week = models.ForeignKey('WeeksTable', models.DO_NOTHING, db_column='id_week')
    attendance_respectfully = models.PositiveIntegerField(blank=True, null=True)
    attendance_disrespectfully = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'attendance_table'
        unique_together = (('id_student', 'id_week'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    key_subgroups = models.ForeignKey('SubgroupsTable', models.DO_NOTHING, db_column='key_subgroups', blank=True, null=True)
    patronymic = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CommentsTable(models.Model):
    id_student = models.OneToOneField('StudentsTable', models.DO_NOTHING, db_column='id_student', primary_key=True)  # The composite primary key (id_student, id_week) found, that is not supported. The first column is selected.
    id_week = models.ForeignKey('WeeksTable', models.DO_NOTHING, db_column='id_week')
    comment = models.CharField(max_length=200, blank=True, null=True)
    color = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments_table'
        unique_together = (('id_student', 'id_week'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class GroupsTable(models.Model):
    id_groups_table = models.AutoField(primary_key=True)
    groups_name = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'groups_table'


class StudentsTable(models.Model):
    id_students_table = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=45)
    key_subgroup = models.ForeignKey('SubgroupsTable', models.DO_NOTHING, db_column='key_subgroup')

    class Meta:
        managed = False
        db_table = 'students_table'


class SubgroupsTable(models.Model):
    id_subgroups_table = models.AutoField(primary_key=True)
    subgroup_name = models.CharField(unique=True, max_length=45)
    key_group = models.ForeignKey(GroupsTable, models.DO_NOTHING, db_column='key_group')

    class Meta:
        managed = False
        db_table = 'subgroups_table'


class WeeksTable(models.Model):
    id_weeks_table = models.AutoField(primary_key=True)
    week_name = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'weeks_table'
