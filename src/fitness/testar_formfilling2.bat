::variables -> URL and STRATEGY_FILE
SET %1
SET %2
SET protocol=webdriver_generic_strategy

cd /d "C:\Users\%USERNAME%\Desktop\TESTAR_dev\testar\target\install\testar\bin" 
testar sse=%protocol% ShowVisualSettingsDialogOnStartup=false Sequences=1 SequenceLength=2 SUTConnectorValue=" ""C:\\windows\\chromedriver.exe"" ""%URL%"" " Mode=Generate StateModelEnabled=false StrategyFile=%STRATEGY_FILE%