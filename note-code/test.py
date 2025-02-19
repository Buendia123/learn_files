import re

# 示例日志内容
log_content = """
WARNING: AL_BASEBOARD_REV not set.  Defaulting to v2.  setup() run?
ERROR: i2c_send_byte(70, 03) (No such device or address)
send_byte(port 1) failed
ERROR: i2c_send_byte(70, 03) (No such device or address)
send_byte(port 2) failed
ERROR: i2c_send_byte(70, 03) (No such device or address)
send_byte(port 3) failed
ERROR: i2c_send_byte(70, 03) (No such device or address)
send_byte(port 4) failed
Checking for presence
Q-1: PRESENT
Q-2: PRESENT
Q-3: -EMPTY-
Q-4: -EMPTY-
Asserting MODSEL on present modules
Identifying modules and steering SWD
Slot 1: QSFP-DD  123456789ABCDEF0 prototype:000001  EM20-04QD-ATB    CA1BA0250111426   MCU:1.19.1.0   DSP:0.0.0.0    MSA:1.37.0      
Slot 2: QSFP+    DT52BSA15PA      VD2CS2451D0E4-S2  EM20-02QA-AUC    CV0CA0244722670   MCU:1.23.2.0   DSP:1.1.31.0   MSA:1.40.0    
ERROR: i2c_send_byte(70, 03) (No such device or address)
ERROR: i2c_send_byte(70, 03) (No such device or address)
ERROR: i2c_send_byte(70, 03) (No such device or address)
ERROR: i2c_send_byte(70, 03) (No such device or address)
--- INA219 Power Monitors --- 
"""

# 模板
form_template = {
    'slot': '0',
    'Type':' ',
    'SN': ' ',
    'PC-SN': ' ',
    'MCU': '0.0.0.0',
    'DSP': '0.0.0.0',
    'MSA': '0.0.0'
}

# 更新正则表达式模式，以匹配模块类型、MCU版本、DSP版本、MSA版本、SN和PC-SN
pattern = re.compile(
    r'Slot\s+(\d+):\s+(QSFP(?:-DD|\+)).*?\s+(\S+)\s+(CA|CV[\w-]+).*?MCU:(\d+\.\d+\.\d+\.\d+)\s+DSP:(\d+\.\d+\.\d+\.\d+)\s+MSA:(\d+\.\d+\.\d+)',
    re.DOTALL
)
pattern_SN = r"QSFP\+?\S+\s+(\S+)\s+(\S+)"

# 使用 findall 方法查找所有匹配项
matche_sn = re.findall(pattern_SN, log_content)

# # 定义存储结果的字典
version = {f"A{i}": form_template.copy() for i in range(1, 5)}

# 从日志中抓取信息
matches = pattern.findall(log_content)

# 将 SN 对应到每个 match 中
for idx, (match, sn_pair) in enumerate(zip(matches, matche_sn)):
    slot_number = int(match[0])
    module_type = match[1]
    
    # 这里是更新 SN 了，sn_pair[1] 是我们从 matche_sn 中提取的 SN 值
    sn = sn_pair[1]  # 例如，'prototype:000001' 或 'VD2CS2451D0E4-S2'
    
    pcsn = match[3]  # PC-SN 以 CA 或 CV 开头
    mcu_version = match[4]
    dsp_version = match[5]
    msa_version = match[6]
    
    if f'A{slot_number}' in version:
        version[f'A{slot_number}'].update({
            "slot": slot_number,
            "Type": module_type,
            "SN": sn,
            "PC-SN": pcsn,
            "MCU": mcu_version,
            "DSP": dsp_version,
            "MSA": msa_version
        })

# 输出抓取的结果
print(version)
