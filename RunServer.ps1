..\VirtualEnviroment\Scripts\activate

$logFilePath = [System.IO.Path]::Combine([System.IO.Directory]::GetCurrentDirectory(), "logs\Logfile.txt");

if(-not [System.IO.File]::Exists($logFilePath)){
    [System.IO.File]::Create($logFilePath);
}

python manage.py runserver;