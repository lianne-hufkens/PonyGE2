@echo off

set URL
set PROTOCOL
set /A ACTIONS
set STRATEGY_FILE

CD /d "C:\Users\%USERNAME%\Desktop\TESTAR_dev\testar\target\install\testar\bin"

testar sse=%PROTOCOL% ShowVisualSettingsDialogOnStartup=false Sequences=1 SequenceLength=%ACTIONS% SUTConnectorValue=" ""C:\\windows\\chromedriver.exe"" ""%URL%"" " Mode=Generate StateModelEnabled=false StrategyFile=%STRATEGY_FILE%