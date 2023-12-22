::variables -> URL and STRATEGY_FILE
SET %1
SET %2
SET protocol=webdriver_generic_strategy

cd /d "C:\Users\%USERNAME%\Desktop\TESTAR_dev\testar\target\install\testar\bin" 
testar sse=%protocol% ShowVisualSettingsDialogOnStartup=false Sequences=1 SequenceLength=2 SUTConnectorValue=" ""C:\\windows\\chromedriver.exe"" ""https://webformsut.testar.org/forms/%URL%"" " Mode=Generate StateModelEnabled=false StrategyFile=settings/webdriver_generic_strategy/%STRATEGY_FILE%