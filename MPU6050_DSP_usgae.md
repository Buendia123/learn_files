# **Hardware**
Author: Buendia.Deng[^1a]  
Rev 1.0  
[^1a]: Buendia.Deng@volex.com 


## DSP API
**Who am i** offset, 0x75. Value, 0x68 Ro

**PWR_MGMT_1** offset, 0x6B,  RW
bit 7: Devcie reset
bit 6: Sleep, low power mode
bit 5: Cycle, wake up frequence

bit 3: TEMP_DIS, disable temperature sensor(1, disable, 0, enable)

bit 0-2: clock source, 0: 8MHz, 1: X Gyro, 2: Y Gyro, 3: Z Gyro, 4: 32.768KHz, 5: 19.2MHz, 6: 26MHz, 7: stop clock,rest

**PWR_MGMT_2** offset, 0x6C,  RW
bit 6-7: LP_WAKE_CTRL, 0: 1.25Hz, 1: 2.5Hz, 2: 5Hz, 3: 20Hz 唤醒频率
bit 0-5: STBY_XA, STBY_YA, STBY_ZA, STBY_XG, STBY_YG, STBY_ZG, 0: enable, 1: disable (stand by 待机模式)

**SMPRT_DIV** offset, 0x19,  RW, sample rate = gryoscope smaple rate/(1+SMPRT_DIV), 当 DLPF is disabled DLPF_CFG=0 DLPF_CFG=0 DLPF_CFG=0 DLPF_CFG=0 or 7），陀螺输出频率=8kHz；当 DLPF is enabled （see 寄存器 0x1A），陀螺仪输出频率=1KHz

**REG_CONFIG** offset, 0x1A,  RW
bit 3-5: EXT_SYNC_SET, 0: disable, 1:TEMP_OUT_L, 2:GYRO_XOUT_L, 3:GYRO_YOUT_L, 4:GYRO_ZOUT_L, 5:ACCEL_XOUT_L, 6:ACCEL_YOUT_L, 7:ACCEL_ZOUT_L (采样引脚，锁存latch的FSYNC作为采样频率)
bit 0-2: DLPF_CFG,acc boardwith 0: 260Hz, 1: 184Hz, 2: 94Hz, 3: 44Hz, 4: 21Hz, 5: 10Hz, 6: 5Hz, 7: reserve, fgyr, 0:256, 1:188, 2:98, 3:42, 4:20, 5:10, 6:5, 7:reserve

**GYRO_CONFIG** offset, 0x1B,  RW
bit 5-7: XG_ST, YG_ST, ZG_ST, 0: disable, 1: enable(self test)
bit 3-4: FS_SEL, 0: 250dps, 1: 500dps, 2: 1000dps, 3: 2000dps

**ACCEL_CONFIG** offset, 0x1C,  RW
bit 5-7: XA_ST, YA_ST, ZA_ST, 0: disable, 1: enable(self test)
bit 3-4: AFS_SEL, 0: 2g, 1: 4g, 2: 8g, 3: 16g

**USER_CTRL** offset, 0x6A,  RW
bit 6:FIFO_EN, 0: disable, 1: enable
bit 5:I2C_MST_EN, 0: disable, 1: enable (1: I2C bus connect other bus interface,0: I2C Control AUX_DA,AUX_CL)
bit 4:I2C_IF_DIS, 0: enable, 1: disable (1: SPI replace I2C)
bit 2:FIFO_RST, 0: no reset, 1: reset
bit 1:I2C_MST_RST, 0: no reset, 1: reset
bit 0:SIG_COND_RST, 0: no reset, 1: reset(1，复位所有传感器的信号通道 (陀螺仪, 加速度计和温度传感器)。这个操作会清除传感器寄存器)

**FIFO_EN** offset, 0x23,  RW
bit 7: TEMP_FIFO_EN, 0: disable, 1: enable
bit 6: XG_FIFO_EN, 0: disable, 1: enable
bit 5: YG_FIFO_EN, 0: disable, 1: enable
bit 4: ZG_FIFO_EN, 0: disable, 1: enable
bit 3: ACCEL_FIFO_EN, 0: disable, 1: enable
bit 2: SLCV2_FIFO_EN, 0: disable, 1: enable(slave 2 fifo)
bit 1: SLCV1_FIFO_EN, 0: disable, 1: enable
bit 0: SLV0_FIFO_EN, 0: disable, 1: enable

**INT_PIN_CFG** offset, 0x37,  RW
bit 7: INT_LEVEL, 0: active low, 1: active high
bit 6: INT_OPEN, 0: push pull, 1: open drain
bit 5: LATCH_INT_EN, 0: disable, 1: enable (锁存中断，0 50us脉冲，1：等待被清除)
bit 4: INT_RD_CLEAR, 0: clear on any read, 1: clear on read of INT_STATUS
bit 3: FSYNC_INT_LEVEL, 0: active low, 1: active high
bit 2: FSYNC_INT_EN, 0: disable, 1: enable
bit 1: I2C_BYPASS_EN, 0: disable, 1: enable（主iic 访问 aux iic使能控制引脚）

**INT_ENABLE** offset, 0x38,  RW
bit 6: MOT_EN, 0: disable, 1: enable
bit 4: FIFO_OFLOW_EN, 0: disable, 1: enable
bit 3: I2C_MST_INT_EN, 0: disable, 1: enable
bit 0: DATA_RDY_EN, 0: disable, 1: enable（Data Ready interrupt）


**INT_STATUS** offset, 0x3A,  RW
bit 7: FIFO_OFLOW_INT, 0: no interrupt, 1: interrupt
bit 6: I2C_MST_INT, 0: no interrupt, 1: interrupt
bit 5: FSYNC_INT, 0: no interrupt, 1: interrupt
bit 4: DATA_RDY_INT, 0: no interrupt, 1: interrupt
bit 0-3: reserved


**ACCEL_XOUT_H** offset, 0x3B,  RW
**ACCEL_XOUT_L** offset, 0x3C,  RW
## DSP usage - github
mpu init
1. Read "Who am i" register to check if the MPU6050 is connected
2. write "PWR_MGMT_1" to 0x80 to reset,read "PWR_MGMT_1" bit 7 to check if the reset is done
3. delay 100ms,  write "PWR_MGMT_1" to 0x01 to set clock source to gyroX
4. write "SMPRT_DIV" to 199 set sample rate to 50Hz
5. write "REG_CONFIG" to 0x03 to set acc bandwith to 44hz,gyo bandwith to 42hz
6. write "PWR_MGMT_1" bit3 set as 0, disable temperature sensor
7. write "PWR_MGMT_1" bit5 set as 0, disable Cycle
8. write "PWR_MGMT_2" bit6 set as 0, use 1.25Hz
9. write "PWR_MGMT_2" bit0-5 set as 0, disable all standby mode
10. write "GYRO_CONFIG" bit 3 set as 3 set gyro full scale to 2000dps
11. write "GYRO_CONFIG" bit 5,6,7 set as 0,0,0, disable gyro self test
12. write "ACCEL_CONFIG" bit3 set as 0 set acc full scale to 2g
12. write "ACCEL_CONFIG" bit 5,6,7 set as 0,0,0, disable gyro self test
13. write "USER_CTRL" bit 6 as 0, disable FIFO
14. write "FIFO_EN" bit 7 as 0, disable temperature sensor
15. write "FIFO_EN" bit 6-3 as 0, disable gyro,accel fifo
16. write "INT_PIN_CFG" bit 7 as 0, active low
17. write "INT_PIN_CFG" bit 6 as 0, push pull

motion interrupt
1. write "INT_ENABLE" bit 6 as 0, disable i2c master interrupt
2. write "INT_ENABLE" bit 4 as 0, disable fifo overflow interrupt
<!-- 3. write "INT_ENABLE" bit 1 as 0, disable data ready interrupt -->
4. write "INT_ENABLE" bit 3 as 0, disable i2c master interrupt
5. write "INT_ENABLE" bit 0 as 1, enable motion interrupt
6. write "INT_PIN_CFG" bit 5 as 0, disable FSYNC interrupt
7. write "INT_PIN_CFG" bit 4 as 0, clear on read
8. write "REG_CONFIG" bit 3 as 0, disable ext sync
9. write "INT_PIN_CFG" bit 2 as 0, disable FSYNC interrupt
10. write "INT_PIN_CFG" bit 3 as 0, FSYNC activate low
11. write "USER_CTRL" bit 5 as 1, enable i2c master
12. write "INT_PIN_CFG" bit 1 as 0, disable aux iic bypass

## DSP usage - vechicle
1. wirte "PWR_MGMT_1" bit 2 as 2, set clock source to PLL with Y axis gyroscope reference
2. write "GYRO_CONFIG" bit 3 set as 3 set gyro full scale to 2000dps
3. write "ACCEL_CONFIG" bit3 set as 0 set acc full scale to 2g
4. write "PWR_MGMT_1" bit 6 as 0, disable sleep mode
5. write "USER_CTRL" bit 5 as 0,  disable i2c master
5. write "INT_PIN_CFG" bit 1 as 0,  disable aux iic bypass

DMP init
1. Read "Who am i" register to check if the MPU6050 is connected
2. write "PWR_MGMT_1" bit 7 as 1, reset
3. delay 100ms,  write "PWR_MGMT_1" bit 0 as 0, set clock source to 8MHz
4. read "accel_offs" 6 bytes ,check byte 5, 3, 1
5. write "GYRO_CONFIG" bit 3 set as 3 set gyro full scale to 2000dps
6. write "ACCEL_CONFIG" bit3 set as 0 set acc full scale to 2g
7. write "REG_CONFIG" to 0x03 to set acc bandwith to 44hz,gyo bandwith to 42hz
8. write "SMPRT_DIV" to 199 set sample rate to 50Hz
9. write "USER_CTRL" bit 6 as 0, disable FIFO


