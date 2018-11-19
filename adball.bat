@echo off

for /f %%i in ('adb devices^|findstr /e "device"') do (
    if "%1" == "shell" (
	    start cmd /k adb -s %%i %*
    ) else (
        adb -s %%i %*
    )
)