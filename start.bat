@echo off
setlocal
chcp 65001 >nul
pushd "%~dp0" || exit /b 1
poetry run streamlit run "app\🤖Welcome.py"
set "app_exit_code=%errorlevel%"
popd
exit /b %app_exit_code%
