set %1
set %2

echo source: %SOURCE%
echo target: %TARGET%

CD /d "C:\Users\%USERNAME%\Desktop\TESTAR_dev\testar\target\install\testar\bin"

testar sse=%PROTOCOL% ShowVisualSettingsDialogOnStartup=false Sequences=1 SequenceLength=%ACTIONS% SUTConnectorValue=" ""C:\\windows\\chromedriver.exe"" ""https://webformsut.testar.org/forms/cb0cb1cb2cb3cb4cb5cb6cb7cb8cb9da3dt1emanf1nu0pasra0seateltextimurlusrwee"" " Mode=Generate StateModelEnabled=false 