# YouTubeL0ader
讓你有效率地下載YouTube的影片和縮圖

# Features
你可以選擇要不要分開下載影片和音檔。而且可以自由選擇要不要下載縮圖。

# How to install?
***首先下載Chocolatey. (https://chocolatey.org/install)
簡單說明:
<br>首先，以管理員身份執行window powersell. <br>
<br>輸入此指令: Get-ExecutionPolicy 如果回傳 **Restricted** 就執行 Set-ExecutionPolicy AllSigned 或 Set-ExecutionPolicy Bypass -Scope Process <br>
<br>然後執行 Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1')) <br>
<br>然後執行 choco install -y yt-dlp ffmpeg lame <br>
<br>最後輸入 pip install pythumb <br>
<br> 最後打開YouTubeL0der.exe便可以使用 <br>
