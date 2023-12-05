f'''
Created on 23 october 2021

@author: Oliva
'''
from dataclasses import dataclass


@dataclass
class Titles(object):
    '''Class for keeping all names for the some language'''
    title: str = "K45"
    Mode_Selection: str = "Mode selection"
    Set: str = "Set"
    Scan: str = "Scan"  #
# -------------------------------------------------------------------------
    PID_Configs: str = "PID Configs"
    Kprop: str = "KP-Proportional part"
    Kdiff: str = "KD-Differential part"
# -------------------------------------------------------------------------
    Scan_configs: str = "Scan configs"
    Scan_time_step: str = "dt - Time Step"
    Scan_temperature_step: str = "dT - Temperature Step"
# -------------------------------------------------------------------------
    Temperatures: str = "Temperatures"
    Measured: str = "Measured"
    Setting_Temperaure: str = "Setting"
    Set_Temperaure: str = "Goal"
# -------------------------------------------------------------------------
    Service_values: str = "Service Values"
    Sensor_Voltage: str = "Sensor Voltage"
# -------------------------------------------------------------------------
    CryoLevel: str = "Cryoliquid Level"
# -------------------------------------------------------------------------
    Status: str = "Status"
    ConnectionState: str = "Current Value"
    HeaterState: str = "Heater"
    CoolerState: str = "Cooler"
    DiodeState: str = "Diode"
# -------------------------------------------------------------------------
    Menu_Connection:str = "Connection"
    Menu_Config:str = "Configuration"
    Menu_Sensor:str = "Sensor"
    Menu_Calibrate:str = "Calibration"
    Menu_Exit:str = "Quit"
# -------------------------------------------------------------------------
    Interface_Configuration:str = "Interface Configuration"
    COM_Port_Selection:str = "COM Port Selection"
    Bauderate_Selection:str = "Bauderate Selection"
# -------------------------------------------------------------------------
    SensorFile: str = "Sensor File"
    Path: str = "Path"
    SensorSendCommand: str = "Send"
    SensorTypeSelect: str = "Sensor Type"
# -------------------------------------------------------------------------
    Calibration: str = "Calibration"
    NullCorrection: str = "Null Correction"
    ADCCoefCorrection_1: str = "ADC Coefficient 1 Correction"
    ADCCoefCorrection_2: str = "ADC Coefficient 2 Correction"
    ADCCoefCorrection_4: str = "ADC Coefficient 4 Correction"
    ADCCoefCorrection_8: str = "ADC Coefficient 8 Correction"
    DAC_Code_10mkA: str      = "DAC Code 10 mkA"
    DAC_Code_10mkA: str      = "DAC Code 25 mkA"
    DAC_Code_100mkA: str     = "DAC Code 100 mkA"
    DAC_Code_250mkA: str     = "DAC Code 250 mkA"

    def __init__(self, Lang):
        '''
        Constructor
        '''
        self.change_language(Lang)

    def change_language(self, Lang):
        
        if Lang == 0:
            self.title = "K45"
            self.Mode_Selection = "Mode selection"
            self.Set = "Set"
            self.Scan = "Scan"  #
            # -----------------------------------------------------------------------
            self.PID_Configs = "PID Configs"
            self.Kprop = "KP-Proportional part"
            self.Kdiff = "KD-Differential part"
            # -----------------------------------------------------------------------
            self.Scan_configs = "Scan configs"
            self.Scan_time_step = "dt - Time Step"
            self.Scan_temperature_step = "dT - Temperature Step"
            # -----------------------------------------------------------------------
            self.Temperatures = "Temperature"
            self.Measured = "Measured"
            self.Setting_Temperaure = "Setting"
            self.Set_Temperaure = "Goal"
            # -----------------------------------------------------------------------
            self.Service_values = "Service Values"
            self.Sensor_Voltage = "Sensor Voltage"
            # -----------------------------------------------------------------------
            self.CryoLevel = "Cryoliquid Level"
            # -----------------------------------------------------------------------
            self.Status = "Status"
            self.ConnectionState = "Connection"
            self.HeaterState = "Heater"
            self.CoolerState = "Cooler"
            self.DiodeState = "Diode"
            # -----------------------------------------------------------------------
            self.Menu_Connection = "Connection"
            self.Menu_Config = "Configuration"
            self.Menu_Sensor = "Sensor"
            self.Menu_Calibrate = "Calibration"
            self.Menu_Exit = "Quit"
            # -------------------------------------------------------------------------
            self.Interface_Configuration = "Interface Configuration"
            self.COM_Port_Selection = "COM Port Selection"
            self.Bouderate_Selection = "Bouderate Selection"
            # -------------------------------------------------------------------------
            self.SensorFile  = "Sensor File"
            self.Path        = "Path"
            self.SensorSendCommand = "Send"
            self.SensorTypeSelect = "Sensor Type"


            # -------------------------------------------------------------------------
            self.Check_access = "Check access"
            self.Enter_Password = "Enter Password"
            # -------------------------------------------------------------------------
            self.Calibration = "Calibration"
            self.NullCorrection = "Null Correction"
            self.ADCCoefCorrection_1 = "ADC Coefficient 1 Correction"
            self.ADCCoefCorrection_2 = "ADC Coefficient 2 Correction"
            self.ADCCoefCorrection_4 = "ADC Coefficient 4 Correction"
            self.ADCCoefCorrection_8 = "ADC Coefficient 8 Correction"
            self.DAC_Code_10mkA      = "DAC Code 10 mkA"
            self.DAC_Code_25mkA      = "DAC Code 25 mkA"
            self.DAC_Code_100mkA     = "DAC Code 100 mkA"
            self.DAC_Code_250mkA     = "DAC Code 250 mkA"

        else:

            self.title = "K45"
            self.Mode_Selection = "Вибір режиму"
            self.Set = "Встановити"
            self.Scan = "Розгортка"
            # -----------------------------------------------------------------------
            self.PID_Configs = "PID параметри"
            self.Kprop = "KP-пропорціональний коефіцієнт"
            self.Kdiff = "KD-диференційний коефіцієнт"
            # -----------------------------------------------------------------------
            self.Scan_configs = "Налаштування розгортки"
            self.Scan_time_step = "dt - Крок по часу"
            self.Scan_temperature_step = "dT - Крок по температурі"
            # -----------------------------------------------------------------------
            self.Temperatures = "Темпетарура"
            self.Measured = "Виміряна"
            self.Setting_Temperaure = "Встановлення"
            self.Set_Temperaure = "Мета"
            # -----------------------------------------------------------------------
            self.Service_values = "Сервісні величини"
            self.Sensor_Voltage = "Напруга на сенсорі"
            # -----------------------------------------------------------------------
            self.CryoLevel = "Рівень кріогента"
            # -----------------------------------------------------------------------
            self.Status = "Статус"
            self.ConnectionState = "Зв'зок"
            self.HeaterState = "Нагрівач"
            self.CoolerState = "Випаровувач"
            self.DiodeState = "Діод"
            # -----------------------------------------------------------------------
            self.Menu_Connection = "Інтерфейс"
            self.Menu_Config = "Конфігурація"
            self.Menu_Sensor = "Сенсор"
            self.Menu_Calibrate = "Калібровка"
            self.Menu_Exit = "Вихід"
            # -------------------------------------------------------------------------
            self.Interface_Configuration = "Налаштування інтерфейсу"
            self.COM_Port_Selection = "COM порт"
            self.Bauderate_Selection = "Швидкість передачі даних"
            # -------------------------------------------------------------------------
            self.SensorFile  = "Файл даних сенсора"
            self.Path        = "Шлях"
            self.SensorSendCommand = "Відправити"
            self.SensorTypeSelect = "Тип сенсора"
            # -------------------------------------------------------------------------
            self.Check_access = "Доступ"
            self.Enter_Password = "Введіть пароль"
            # -------------------------------------------------------------------------
            self.Calibration = "Калібровка"
            self.NullCorrection = "Корекція нуля"
            self.ADCCoefCorrection_1 = "Корекція АЦП K = 1 "
            self.ADCCoefCorrection_2 = "Корекція АЦП K = 2 "
            self.ADCCoefCorrection_4 = "Корекція АЦП K = 4 "
            self.ADCCoefCorrection_8 = "Корекція АЦП K = 8 "
            self.DAC_Code_10mkA      = "Код ЦАП 10 mkA"
            self.DAC_Code_25mkA      = "Код ЦАП 25 mkA"
            self.DAC_Code_100mkA     = "Код ЦАП 100 mkA"
            self.DAC_Code_250mkA     = "Код ЦАП 250 mkA"


