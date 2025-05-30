# Generated by Django 4.2.20 on 2025-05-06 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("workhub", "0007_jobscrap"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobpost",
            name="education",
            field=models.CharField(
                choices=[
                    ("highschool", "고졸"),
                    ("college", "초대졸"),
                    ("bachelor", "대졸"),
                    ("master", "석사 이상"),
                ],
                default="bachelor",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="jobpost",
            name="experience",
            field=models.CharField(
                choices=[
                    ("entry", "신입"),
                    ("mid", "1~3년차"),
                    ("senior", "4~7년차"),
                    ("expert", "8년 이상"),
                ],
                default="entry",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="resume",
            name="education",
            field=models.CharField(
                choices=[
                    ("highschool", "고졸"),
                    ("college", "초대졸"),
                    ("bachelor", "대졸"),
                    ("master", "석사 이상"),
                ],
                default="bachelor",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="resume",
            name="experience",
            field=models.CharField(
                choices=[
                    ("entry", "신입"),
                    ("mid", "1~3년차"),
                    ("senior", "4~7년차"),
                    ("expert", "8년 이상"),
                ],
                default="entry",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="resume",
            name="preferred_location",
            field=models.CharField(
                choices=[
                    ("seoul", "서울"),
                    ("busan", "부산"),
                    ("incheon", "인천"),
                    ("daegu", "대구"),
                    ("gyeonggi", "경기"),
                    ("etc", "상관없음"),
                ],
                default="seoul",
                max_length=20,
                verbose_name="근무 가능 지역",
            ),
        ),
        migrations.AlterField(
            model_name="jobpost",
            name="location",
            field=models.CharField(
                choices=[
                    ("seoul", "서울"),
                    ("busan", "부산"),
                    ("incheon", "인천"),
                    ("daegu", "대구"),
                    ("gyeonggi", "경기"),
                    ("etc", "상관없음"),
                ],
                max_length=100,
            ),
        ),
    ]
