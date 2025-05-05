@echo off
REM Set the base URL
set BASE_URL=http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com

REM Set WebArena environment variables
set WA_SHOPPING=%BASE_URL%:7770/
set WA_SHOPPING_ADMIN=%BASE_URL%:7780/admin
set WA_REDDIT=%BASE_URL%:9999
set WA_GITLAB=%BASE_URL%:8023
set WA_WIKIPEDIA=%BASE_URL%:8081/wikipedia_en_all_maxi_2022-05/A/User:The_other_Kiwix_guy/Landing
set WA_MAP=%BASE_URL%:3000
set WA_HOMEPAGE=%BASE_URL%:4399

REM If FULL_RESET is available, uncomment the line below:
REM set WA_FULL_RESET=%BASE_URL%:7565

REM Otherwise, leave it empty
set WA_FULL_RESET=


rem HOME = "http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:4399/"
rem #     MAP = "http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:3000/#map=7/42.896/-75.108/"
rem #     REDDIT = "http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:9999/forums/all"
rem #     GITLAB = "http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:8023/explore/"
rem #     SHOPPING = "http://ec2-18-190-119-92.us-east-2.compute.amazonaws.com:7770/"