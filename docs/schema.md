# Database Schema Overview

This document summarizes the SQLAlchemy models used in the backend.

## Regions
- **Table:** `regions`
- **Columns:**
  - `id` – primary key
  - `name` – region name
- **Relationships:** each region has many `cities` (cascade delete-orphan).

## Cities
- **Table:** `cities`
- **Columns:**
  - `id` – primary key
  - `name` – city name
  - `region_id` – FK to `regions.id` (CASCADE)
- **Relationships:** belongs to `Region`, has many `schools` (cascade delete-orphan).

## Schools
- **Table:** `schools`
- **Columns:**
  - `id` – primary key
  - `name` – school name
  - `full_name` – optional official name
  - `city_id` – FK to `cities.id` (CASCADE)
- **Relationships:** belongs to `City`, has `students`, `teachers`, `schedules`, `subjects` and `classes` (cascade delete-orphan).

## AcademicYear
- **Table:** `academic_years`
- **Columns:**
  - `id` – primary key
  - `year_start`, `year_end` – dates
  - `name` – textual label
- **Relationships:** has many `schedules`, `grades`, `attendance_records`, `classes`, `teacher_subjects` and `class_teachers` (cascade delete-orphan).

## Students
- **Table:** `students`
- **Columns:**
  - `id` – primary key
  - `full_name`
  - `class_name`
  - `class_id` – FK to `classes.id` (CASCADE)
  - `parent_id` – FK to `parents.id` (SET NULL)
  - `contact_info`
  - `school_id` – FK to `schools.id` (CASCADE)
- **Relationships:** belongs to `Parent`, `School` and `Class`. Has `grades` and `attendance_records` (cascade delete-orphan).

## Teachers
- **Table:** `teachers`
- **Columns:**
  - `id` – primary key
  - `full_name`
  - `contact_info`
  - `school_id` – FK to `schools.id` (CASCADE)
  - `is_active` – boolean flag, defaults to true
- **Relationships:** many-to-many with `Subject` via `teacher_subjects`. Has `grades`, `schedules`, `classes` and `class_teachers` (cascade delete-orphan).

## Subjects
- **Table:** `subjects`
- **Columns:**
  - `id` – primary key
  - `name` – unique
  - `school_id` – FK to `schools.id`
- **Relationships:** belongs to `School`, many-to-many with `Teacher` via `teacher_subjects` and with `Class` via `class_subjects`. Has `grades` and `schedules`.

## TeacherSubject
- **Table:** `teacher_subjects`
- **Columns:**
  - `teacher_id` – PK & FK to `teachers.id` (CASCADE)
  - `subject_id` – PK & FK to `subjects.id` (CASCADE)
  - `academic_year_id` – PK & FK to `academic_years.id` (CASCADE)
- **Purpose:** association table between teachers and subjects.

## Parents
- **Table:** `parents`
- **Columns:**
  - `id` – primary key
  - `first_name`, `last_name`
  - `contact_info`
- **Relationships:** one-to-many with `Student` (children are not deleted with parent).

## Grades
- **Table:** `grades`
- **Columns:**
  - `id` – primary key
  - `value`
  - `date`
  - `student_id` – FK to `students.id` (CASCADE)
  - `teacher_id` – FK to `teachers.id` (CASCADE)
  - `subject_id` – FK to `subjects.id` (RESTRICT)
  - `academic_year_id` – FK to `academic_years.id` (CASCADE)
- **Relationships:** belongs to `Student`, `Teacher`, `Subject` and `AcademicYear`.

## Schedules
- **Table:** `schedules`
- **Columns:**
  - `id` – primary key
  - `date`
  - `class_name`
  - `teacher_id` – FK to `teachers.id` (CASCADE)
  - `subject_id` – FK to `subjects.id` (RESTRICT)
  - `school_id` – FK to `schools.id` (CASCADE)
  - `academic_year_id` – FK to `academic_years.id` (CASCADE)
- **Relationships:** belongs to `Teacher`, `Subject`, `School` and `AcademicYear`.

## Attendance
- **Table:** `attendance`
- **Columns:**
  - `id` – primary key
  - `date`
  - `is_present`
  - `student_id` – FK to `students.id` (CASCADE)
  - `academic_year_id` – FK to `academic_years.id` (CASCADE)
- **Relationships:** belongs to `Student` and `AcademicYear`.

## Administrators
- **Table:** `administrators`
- **Columns:**
  - `id` – primary key
  - `name`
  - `login` – unique
  - `password_hash`
  - `rights`

## Classes
- **Table:** `classes`
- **Columns:**
  - `id` – primary key
  - `name` – unique
  - `school_id` – FK to `schools.id` (CASCADE)
  - `academic_year_id` – FK to `academic_years.id` (CASCADE)
  - `is_archived` – boolean flag, defaults to false
- **Relationships:** has many `students`, many-to-many with `Subject` via `class_subjects` and with `Teacher` via `class_teachers`. `class_teachers` records determine homeroom, assistant or regular teachers.

## ClassSubject
- **Table:** `class_subjects`
- **Columns:**
  - `class_id` – PK & FK to `classes.id` (CASCADE)
  - `subject_id` – PK & FK to `subjects.id` (CASCADE)
- **Purpose:** association table between classes and subjects.

## ClassTeacher
- **Table:** `class_teachers`
- **Columns:**
  - `class_id` – PK & FK to `classes.id` (CASCADE)
  - `teacher_id` – PK & FK to `teachers.id` (CASCADE)
  - `academic_year_id` – PK & FK to `academic_years.id` (CASCADE)
- **Purpose:** base relation between teacher and class for a year.

## ClassTeacherRoleAssociation
- **Table:** `class_teacher_roles`
- **Columns:**
  - `class_id` – FK to `class_teachers.class_id`
  - `teacher_id` – FK to `class_teachers.teacher_id`
  - `academic_year_id` – FK to `class_teachers.academic_year_id`
  - `role` – Enum `ClassTeacherRole`
- **Purpose:** stores roles for class-teacher relation. Unique index ensures one homeroom teacher per class and academic year.

## Users
- **Table:** `users`
- **Columns:**
  - `id` – primary key
  - `username` – unique
  - `password_hash`
  - `role` – Enum `RoleEnum`

### Enumerations
- **RoleEnum:** defines user roles (`superuser`, `administrator`, `teacher`, `student`, `parent`).
- **ClassTeacherRole:** roles for class-teacher relations (`regular`, `homeroom`, `assistant`).

Cascade behaviors are mainly used on foreign keys with `ondelete='CASCADE'` to automatically remove dependent records.
