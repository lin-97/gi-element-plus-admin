@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"
set "REPO_ROOT=%SCRIPT_DIR%.."

rem 获取真实的 ANSI ESC 字符，避免直接输出裸的 [0;31m 这类颜色码。
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$E# & echo on & for %%b in (1) do rem"') do set "ESC=%%b"

rem 新版 Windows 终端支持 ANSI 颜色；如果获取失败，则退回无色输出。
if defined ESC (
    set "tty_red=!ESC![0;31m"
    set "tty_green=!ESC![0;32m"
    set "tty_yellow=!ESC![0;33m"
    set "tty_blue=!ESC![0;34m"
    set "tty_cyan=!ESC![0;36m"
    set "tty_purple=!ESC![0;35m"
    set "tty_bold=!ESC![1m"
    set "tty_reset=!ESC![0m"

    set "RED=!ESC![0;31m"
    set "GREEN=!ESC![0;32m"
    set "YELLOW=!ESC![33m"
    set "BLUE=!ESC![0;34m"
    set "CYAN=!ESC![0;36m"
    set "LIGHT_GRAY=!ESC![0;37m"
    set "PURPLE=!ESC![0;35m"
    set "BOLD=!ESC![1m"
    set "RESET=!ESC![0m"
) else (
    set "tty_red="
    set "tty_green="
    set "tty_yellow="
    set "tty_blue="
    set "tty_cyan="
    set "tty_purple="
    set "tty_bold="
    set "tty_reset="

    set "RED="
    set "GREEN="
    set "YELLOW="
    set "BLUE="
    set "CYAN="
    set "LIGHT_GRAY="
    set "PURPLE="
    set "BOLD="
    set "RESET="
)

if /i "%~1"=="--start-dev" (
    call :start_dev_server
    exit /b !errorlevel!
)

goto :main_menu

:info
echo !tty_green!OK: %~1!tty_reset!
goto :eof

:warn
echo !tty_yellow!WARNING: %~1!tty_reset!
goto :eof

:error
echo !tty_red!ERROR: %~1!tty_reset!
goto :eof

:pause
pause
goto :eof

:JudgeSuccess
if errorlevel 1 (
    call :error "步骤失败: %~1"
    exit /b 1
) else (
    call :info "步骤成功: %~1"
)
exit /b 0

:print_separator
echo !LIGHT_GRAY!---------------------------------------------------------------------!RESET!
goto :eof

:show_banner
echo.
echo +----------------------------------------------+
echo ^|         !tty_blue!欢迎使用 Gi Admin 初始化脚本!tty_reset!          ^|
echo +----------------------------------------------+
echo 版本: 3.0.0
echo 作者：coderxslee
echo.
goto :eof

:trim
set "_trim=!%~1!"
for /f "tokens=* delims= " %%a in ("!_trim!") do set "_trim=%%a"
:trim_tail
if defined _trim if "!_trim:~-1!"==" " (
    set "_trim=!_trim:~0,-1!"
    goto :trim_tail
)
set "%~1=!_trim!"
exit /b 0

:lower
set "_lower=!%~1!"
for %%a in (A=a B=b C=c D=d E=e F=f G=g H=h I=i J=j K=k L=l M=m N=n O=o P=p Q=q R=r S=s T=t U=u V=v W=w X=x Y=y Z=z) do (
    for /f "tokens=1,2 delims==" %%b in ("%%a") do set "_lower=!_lower:%%b=%%c!"
)
set "%~1=!_lower!"
exit /b 0

:read_env_value
set "_key=%~1"
set "_out=%~2"
set "%_out%="

rem 读取 .env.dev 中的 KEY=VALUE，并去掉行内注释和首尾空格。
for /f "usebackq tokens=1,* delims==" %%a in ("%env_file%") do (
    set "_env_key=%%a"
    set "_env_value=%%b"
    call :trim _env_key
    if "!_env_key!"=="!_key!" (
        for /f "tokens=1 delims=#" %%c in ("!_env_value!") do set "_env_value=%%c"
        call :trim _env_value
        set "%_out%=!_env_value!"
    )
)
exit /b 0

:load_db_config
set "env_file=%SCRIPT_DIR%env\.env.dev"

if not exist "%env_file%" (
    call :error "未找到 %env_file% 文件"
    exit /b 1
)

set "DATABASE_TYPE="
set "DATABASE_HOST="
set "DATABASE_PORT="
set "DATABASE_USER="
set "DATABASE_PASSWORD="
set "DATABASE_NAME="

call :read_env_value "DATABASE_TYPE" "DATABASE_TYPE"
if "!DATABASE_TYPE!"=="" set "DATABASE_TYPE=mysql"
call :lower DATABASE_TYPE

rem 与 Linux 脚本保持一致：mariadb 走 mysql 配置，postgresql 走 postgres 配置。
if "!DATABASE_TYPE!"=="mariadb" set "DATABASE_TYPE=mysql"
if "!DATABASE_TYPE!"=="postgresql" set "DATABASE_TYPE=postgres"

if "!DATABASE_TYPE!"=="mysql" (
    call :read_env_value "MYSQL_HOST" "DATABASE_HOST"
    call :read_env_value "MYSQL_PORT" "DATABASE_PORT"
    call :read_env_value "MYSQL_USER" "DATABASE_USER"
    call :read_env_value "MYSQL_PASSWORD" "DATABASE_PASSWORD"
    call :read_env_value "MYSQL_DATABASE" "DATABASE_NAME"
    if "!DATABASE_PORT!"=="" set "DATABASE_PORT=3306"
) else if "!DATABASE_TYPE!"=="postgres" (
    call :read_env_value "POSTGRES_HOST" "DATABASE_HOST"
    call :read_env_value "POSTGRES_PORT" "DATABASE_PORT"
    call :read_env_value "POSTGRES_USER" "DATABASE_USER"
    call :read_env_value "POSTGRES_PASSWORD" "DATABASE_PASSWORD"
    call :read_env_value "POSTGRES_DATABASE" "DATABASE_NAME"
    if "!DATABASE_PORT!"=="" set "DATABASE_PORT=5432"
) else (
    call :error "不支持的数据库类型: !DATABASE_TYPE!"
    exit /b 1
)

if "!DATABASE_HOST!"=="" (
    call :error "数据库配置不完整，请检查 %env_file% 文件"
    exit /b 1
)
if "!DATABASE_PORT!"=="" (
    call :error "数据库配置不完整，请检查 %env_file% 文件"
    exit /b 1
)
if "!DATABASE_USER!"=="" (
    call :error "数据库配置不完整，请检查 %env_file% 文件"
    exit /b 1
)
if "!DATABASE_NAME!"=="" (
    call :error "数据库配置不完整，请检查 %env_file% 文件"
    exit /b 1
)

exit /b 0

:mysql_exec
set "_sql=%~1"
set "_db=%~2"
set "_db_arg="
if not "!_db!"=="" set "_db_arg=-D!_db!"

if not "!DATABASE_PASSWORD!"=="" (
    set "MYSQL_PWD=!DATABASE_PASSWORD!"
    mysql -h"!DATABASE_HOST!" -P"!DATABASE_PORT!" -u"!DATABASE_USER!" !_db_arg! -e "!_sql!"
    set "_mysql_error=!errorlevel!"
    set "MYSQL_PWD="
    exit /b !_mysql_error!
)

mysql -h"!DATABASE_HOST!" -P"!DATABASE_PORT!" -u"!DATABASE_USER!" !_db_arg! -e "!_sql!"
exit /b !errorlevel!

:ensure_database_exists
if "!DATABASE_TYPE!"=="mysql" (
    rem MySQL 使用幂等建库语句，已存在时不会修改现有数据库。
    call :mysql_exec "CREATE DATABASE IF NOT EXISTS `!DATABASE_NAME!` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    if errorlevel 1 exit /b 1
    call :info "数据库 '!DATABASE_NAME!' 已就绪"
    exit /b 0
)

if "!DATABASE_TYPE!"=="postgres" (
    set "db_exists="
    set "PGPASSWORD=!DATABASE_PASSWORD!"
    rem PostgreSQL 不能直接 CREATE DATABASE IF NOT EXISTS，先查再按需创建。
    for /f "usebackq delims=" %%a in (`psql -h "!DATABASE_HOST!" -p "!DATABASE_PORT!" -U "!DATABASE_USER!" -d "postgres" -tAc "SELECT 1 FROM pg_database WHERE datname='!DATABASE_NAME!';" 2^>nul`) do set "db_exists=%%a"
    if not "!db_exists!"=="1" (
        call :warn "数据库 '!DATABASE_NAME!' 不存在，正在创建..."
        psql -h "!DATABASE_HOST!" -p "!DATABASE_PORT!" -U "!DATABASE_USER!" -d "postgres" -c "CREATE DATABASE ""!DATABASE_NAME!"" WITH ENCODING 'UTF8' LC_COLLATE 'C.UTF-8' LC_CTYPE 'C.UTF-8' TEMPLATE template0 OWNER !DATABASE_USER!;"
        if errorlevel 1 (
            set "PGPASSWORD="
            exit /b 1
        )
    )
    set "PGPASSWORD="
    call :info "数据库 '!DATABASE_NAME!' 已就绪"
    exit /b 0
)

exit /b 1

:start_dev_server
call :print_separator
echo 启动（uv run dev）...

call :load_db_config
if errorlevel 1 exit /b 1

echo 检查并创建数据库...
call :ensure_database_exists
if errorlevel 1 exit /b 1

call :print_separator
cd /d "%SCRIPT_DIR%"
uv run main.py run --env=dev
call :JudgeSuccess "开发服务器启动" || exit /b 1

echo 开发服务器启动完成！
call :print_separator
exit /b 0

:create_migration
call :print_separator
echo 生成迁移文件（模型变更后）...

cd /d "%SCRIPT_DIR%"
uv run main.py revision --env=dev
call :JudgeSuccess "迁移文件生成" || exit /b 1

echo 迁移文件生成完成！
call :print_separator
exit /b 0

:apply_migration
call :print_separator
echo 应用迁移...

cd /d "%SCRIPT_DIR%"
uv run main.py upgrade --env=dev
call :JudgeSuccess "迁移应用" || exit /b 1

echo 迁移应用完成！
call :print_separator
exit /b 0

:reset_migration_records
call :print_separator
echo 重置数据库中的迁移记录...

echo 警告：此操作将重置数据库中的迁移记录！
set /p confirm="确认继续吗？(y/N): "
if /i not "!confirm!"=="y" (
    echo 操作已取消
    exit /b 0
)

call :load_db_config
if errorlevel 1 exit /b 1

cd /d "%SCRIPT_DIR%"
echo 正在重置迁移记录...

set "PGPASSWORD=!DATABASE_PASSWORD!"
psql -h "!DATABASE_HOST!" -p "!DATABASE_PORT!" -U "!DATABASE_USER!" -d "!DATABASE_NAME!" -c "DELETE FROM alembic_version;"
set "_psql_error=!errorlevel!"
set "PGPASSWORD="
if not "!_psql_error!"=="0" exit /b !_psql_error!
call :JudgeSuccess "迁移记录重置" || exit /b 1

echo 迁移记录重置完成！
call :print_separator
exit /b 0

:clean_database
call :print_separator
echo 清理数据库（删除所有表）...

echo 警告：此操作将删除数据库中的所有数据！
set /p confirm="确认继续吗？(y/N): "
if /i not "!confirm!"=="y" (
    echo 操作已取消
    exit /b 0
)

call :load_db_config
if errorlevel 1 exit /b 1

cd /d "%SCRIPT_DIR%"
echo 清理数据库，删除所有现有的表...

set "PGPASSWORD=!DATABASE_PASSWORD!"
psql -h "!DATABASE_HOST!" -p "!DATABASE_PORT!" -U "!DATABASE_USER!" -d "!DATABASE_NAME!" -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
set "_psql_error=!errorlevel!"
set "PGPASSWORD="
if not "!_psql_error!"=="0" exit /b !_psql_error!
call :JudgeSuccess "数据库清理" || exit /b 1

echo 数据库清理完成！
call :print_separator
exit /b 0

:drop_database
call :print_separator
echo 删除数据库...

echo 请输入要删除的数据库名称:
set /p db_name="数据库名称: "

if "!db_name!"=="" (
    call :error "数据库名称不能为空！"
    exit /b 1
)

echo 警告：此操作将永久删除数据库 '!db_name!' 及其所有数据！
echo 此操作不可撤销！

set /p confirm1="确认要删除数据库 '!db_name!' 吗？(y/N): "
if /i not "!confirm1!"=="y" (
    echo 操作已取消
    exit /b 0
)

echo 最后确认：您真的要删除数据库 '!db_name!' 吗？
set /p confirm2="请输入 'DELETE' 来确认删除: "
if /i not "!confirm2!"=="DELETE" (
    echo 操作已取消
    exit /b 0
)

call :load_db_config
if errorlevel 1 exit /b 1

cd /d "%SCRIPT_DIR%"
echo 正在删除数据库 '!db_name!'...

set "PGPASSWORD=!DATABASE_PASSWORD!"
psql -h "!DATABASE_HOST!" -p "!DATABASE_PORT!" -U "!DATABASE_USER!" -d "postgres" -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '!db_name!' AND pid <> pg_backend_pid();"
psql -h "!DATABASE_HOST!" -p "!DATABASE_PORT!" -U "!DATABASE_USER!" -d "postgres" -c "DROP DATABASE IF EXISTS ""!db_name!"";"
set "_psql_error=!errorlevel!"
set "PGPASSWORD="
if not "!_psql_error!"=="0" exit /b !_psql_error!
call :JudgeSuccess "数据库删除" || exit /b 1

echo 数据库 '!db_name!' 删除完成！
call :print_separator
exit /b 0

:init_sql_data
call :print_separator
echo 初始化数据...

set "sql_dir=%REPO_ROOT%\backend\sql\postgres\init_data"

if not exist "%sql_dir%\" (
    call :error "未找到 SQL 目录: %sql_dir%"
    exit /b 1
)

set "file_count=0"
rem 按文件名排序，保持和 Linux find | sort 的执行顺序一致。
for /f "delims=" %%f in ('dir /b /a-d /on "%sql_dir%\*.sql" 2^>nul') do (
    set /a file_count+=1
    set "sql_file_!file_count!=%sql_dir%\%%f"
    set "sql_name_!file_count!=%%f"
)

if "!file_count!"=="0" (
    call :warn "SQL 目录下没有可执行的 .sql 文件: %sql_dir%"
    exit /b 0
)

echo 可用 SQL 文件：
echo 0. 执行全部 SQL 文件
for /l %%i in (1,1,!file_count!) do echo %%i. !sql_name_%%i!

set /p choice="请选择要初始化的 SQL（输入序号）: "

echo !choice!| findstr /r "^[0-9][0-9]*$" >nul
if errorlevel 1 (
    call :error "输入无效，请输入数字序号"
    exit /b 1
)

call :load_db_config
if errorlevel 1 exit /b 1

if "!choice!"=="0" (
    echo 开始执行全部 SQL 文件...
    for /l %%i in (1,1,!file_count!) do (
        echo 执行: !sql_name_%%i!
        set "PGPASSWORD=!DATABASE_PASSWORD!"
        psql -h "!DATABASE_HOST!" -p "!DATABASE_PORT!" -U "!DATABASE_USER!" -d "!DATABASE_NAME!" -f "!sql_file_%%i!"
        set "_psql_error=!errorlevel!"
        set "PGPASSWORD="
        if not "!_psql_error!"=="0" (
            call :error "执行失败: !sql_name_%%i!"
            exit /b !_psql_error!
        )
        call :info "执行成功: !sql_name_%%i!"
    )
    call :info "全部 SQL 文件执行完成"
) else (
    if !choice! LSS 1 (
        call :error "序号超出范围"
        exit /b 1
    )
    if !choice! GTR !file_count! (
        call :error "序号超出范围"
        exit /b 1
    )

    echo 执行: !sql_name_%choice%!
    set "PGPASSWORD=!DATABASE_PASSWORD!"
    psql -h "!DATABASE_HOST!" -p "!DATABASE_PORT!" -U "!DATABASE_USER!" -d "!DATABASE_NAME!" -f "!sql_file_%choice%!"
    set "_psql_error=!errorlevel!"
    set "PGPASSWORD="
    if not "!_psql_error!"=="0" (
        call :error "执行失败: !sql_name_%choice%!"
        exit /b !_psql_error!
    )
    call :info "执行成功: !sql_name_%choice%!"
    call :info "SQL 初始化完成"
)

call :print_separator
exit /b 0

:main_menu
cls
call :show_banner
echo 请选择要执行的操作：
echo.
echo 1. 启动（uv run dev）
echo 2. 生成迁移文件（模型变更后）
echo 3. 应用迁移
echo 4. 重置数据库中的迁移记录
echo 5. 清理数据库（删除所有表）
echo 6. 删除数据库
echo 7. 初始化数据（执行 sql 脚本）
echo 0. 退出
echo.

set /p option="请选择你要执行的操作: "

if "!option!"=="1" call :start_dev_server
if "!option!"=="2" call :create_migration
if "!option!"=="3" call :apply_migration
if "!option!"=="4" call :reset_migration_records
if "!option!"=="5" call :clean_database
if "!option!"=="6" call :drop_database
if "!option!"=="7" call :init_sql_data
if "!option!"=="0" exit /b 0

if not "!option!"=="1" if not "!option!"=="2" if not "!option!"=="3" if not "!option!"=="4" if not "!option!"=="5" if not "!option!"=="6" if not "!option!"=="7" (
    call :error "未知选项: !option!"
)

call :pause
goto :main_menu
