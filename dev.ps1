<#
.SYNOPSIS
    找 Ren'Py SDK 并跑本工程。依赖清单见 依赖.md。

.EXAMPLE
    .\dev.ps1 lint
    .\dev.ps1 test
    .\dev.ps1 run
    .\dev.ps1 compile
    .\dev.ps1 distribute
#>
param(
    [Parameter(Position = 0)]
    [ValidateSet('run', 'lint', 'compile', 'test', 'distribute')]
    [string]$Command = 'lint',

    # test 用：只跑某个 testcase
    [Parameter(Position = 1)]
    [string]$Name = ''
)

$ErrorActionPreference = 'Stop'
$repo = $PSScriptRoot

function Find-Sdk {
    # 只认两类位置：显式设的 $env:RENPY_SDK，和仓库旁边两个固定目录。
    # 不扫 C:\、D:\、%LOCALAPPDATA% 这类可写目录：谁往那儿放一个带 renpy.py 的文件夹，
    # 就会连带执行里面的 python.exe。
    $candidates = @()

    if ($env:RENPY_SDK) { $candidates += $env:RENPY_SDK }
    $candidates += (Join-Path (Split-Path $repo -Parent) 'tools\renpy-8.5.3-sdk')
    $candidates += (Join-Path (Split-Path $repo -Parent) 'renpy-8.5.3-sdk')

    foreach ($c in $candidates) {
        if (-not $c) { continue }
        if (Test-Path (Join-Path $c 'renpy.py')) { return (Resolve-Path $c).Path }
    }

    Write-Host "没找到 Ren'Py 8.5.3 SDK。" -ForegroundColor Red
    Write-Host "下载：https://www.renpy.org/dl/8.5.3/renpy-8.5.3-sdk.zip （解压即可，不用安装）" -ForegroundColor Yellow
    Write-Host "然后二选一：" -ForegroundColor Yellow
    Write-Host '  $env:RENPY_SDK = "D:\renpy-8.5.3-sdk"'
    Write-Host "  或者把它放到  $((Split-Path $repo -Parent))\tools\renpy-8.5.3-sdk"
    exit 1
}

$sdk = Find-Sdk
$py = Join-Path $sdk 'lib\py3-windows-x86_64\python.exe'

Write-Host "SDK : $sdk"
Write-Host "工程: $repo"
Write-Host "命令: $Command"

switch ($Command) {
    'run' {
        # 沙箱里跑不了 %APPDATA% 时，调用方自己设 $env:RENPY_PATH_TO_SAVES
        & (Join-Path $sdk 'renpy.exe') $repo
    }
    'distribute' {
        & $py (Join-Path $sdk 'renpy.py') $repo distribute
    }
    default {
        $argList = @((Join-Path $sdk 'renpy.py'), $repo, $Command)
        if ($Command -eq 'test' -and $Name) { $argList += $Name }
        & $py @argList
    }
}

exit $LASTEXITCODE
