import pandas as pd
import numpy as np
from natsort import natsort_keygen

path = input('Enter filename : ')
hour = input('Enter hour : ')
minute = input('Enter minute : ')

df = pd.read_excel(rF'./{path}.xlsx')
minute = int(minute) + (int(hour) * 60)
time_min = int(minute) * 3
#clean data
df = df.drop(df[df['ส่งของแล้ว (ออเดอร์)'] == True].index)
df = df.drop(df[df['พิมพ์แล้ว (ออเดอร์)'] == True].index)
df = df.drop(df[df['ยืนยันการชำระเงินแล้ว (ออเดอร์)'] == False].index)
df = df.drop(df[df['ยกเลิก'] == True].index)
df = df.drop(df[df['ชื่อ (ออเดอร์)'] == 'ขายหน้าร้าน'].index)

#split order track
df['old'], df['split'] = df['เลขที่ออเดอร์ (ออเดอร์)'].str.split('-').str

#sort value
df = df.sort_values(by=['split'], key=natsort_keygen())

#เหลือใส่เลขออเดอร์
df.insert(4, 'จำนวน', '-', True)

#add value
df['จำนวน'] = np.where(df['จำนวนที่ซื้อ'] == 2, 'สองตัว', df['จำนวน'])
df['จำนวน'] = np.where(df['จำนวนที่ซื้อ'] == 3, 'สามตัว', df['จำนวน'])
df['จำนวน'] = np.where(df['จำนวนที่ซื้อ'] == 4, 'สี่ตัว', df['จำนวน'])
df['จำนวน'] = np.where(df['จำนวนที่ซื้อ'] > 4, 'ดูหน้าซอง', df['จำนวน'])

df.insert(5, 'SP_CHECK', '', True)
df.insert(5, 'EE_CHECK', '', True)

df['SP_CHECK'] = np.where(df['ชื่อ (ออเดอร์)'].str.find('SP') >= 0, 'SP', df['SP_CHECK'])

df['EE_CHECK'] = np.where(df['หมายเหตุ (ออเดอร์)'].str.find('old') >= 0, 'EE', df['EE_CHECK'])
df['EE_CHECK'] = np.where(df['หมายเหตุ (ออเดอร์)'].str.find('Old') >= 0, 'EE', df['EE_CHECK'])
df['EE_CHECK'] = np.where(df['หมายเหตุ (ออเดอร์)'].str.find('OLD') >= 0, 'EE', df['EE_CHECK'])

#drop
df = df.drop('old', 1)
df = df.drop('split', 1)
df = df.drop('ส่งของแล้ว (ออเดอร์)', 1)
df = df.drop('พิมพ์แล้ว (ออเดอร์)', 1)
df = df.drop('วันที่พิมพ์ (ออเดอร์)', 1)
df = df.drop('ยืนยันการชำระเงินแล้ว (ออเดอร์)', 1)
df = df.drop('พรีออเดอร์ (ออเดอร์)', 1)
df = df.drop('ยกเลิก', 1)
df = df.drop('ข้อมูลชื่อที่อยู่ครบถ้วน (ออเดอร์)', 1)
df = df.drop('เลขพัสดุ (ออเดอร์)', 1)
df = df.drop('ยกเลิกออเดอร์แล้ว (ออเดอร์)', 1)
df = df.drop('วันที่ยกเลิกออเดอร์ (ออเดอร์)', 1)
df = df.drop('ราคา', 1)
df = df.drop('ส่วนลดต่อหน่วย', 1)
df = df.drop('วันที่โอนเงิน (ออเดอร์)', 1)
df = df.drop('ยอดโอน (ออเดอร์)', 1)
df = df.drop('ยอด COD (ออเดอร์)', 1)
df = df.drop('ยอดขาย (ออเดอร์)', 1)
df = df.drop('ค่าส่งที่เก็บลูกค้า (ออเดอร์)', 1)
df = df.drop('เบอร์โทร (ออเดอร์)', 1)
df = df.drop('ขนส่ง (ออเดอร์)', 1)
df = df.drop('ธนาคารที่รับเงิน (ออเดอร์)', 1)
df = df.drop('วันที่สร้าง', 1)
df = df.drop('ชื่อสินค้า (สินค้า)', 1)
df = df.drop('ชื่อ (สินค้าย่อย)', 1)

df.to_excel(r'Export.xlsx', index = False)
df = pd.read_excel(r'Export.xlsx')

#assing worker
df.insert(2, 'คนแพค', '', True)
df.insert(2, 'non_check', False, True)

#check slase
df['non_check'] = np.where(df['รหัส (สินค้าย่อย)'].str.find('A') == 0, True, df['non_check'])
df['non_check'] = np.where(df['รหัส (สินค้าย่อย)'].str.find('SK') == 0, True, df['non_check'])
df['non_check'] = np.where(df['รหัส (สินค้าย่อย)'].str.find('Y') == 0, True, df['non_check'])
df['non_check'] = np.where(df['รหัส (สินค้าย่อย)'].str.find('D') == 0, True, df['non_check'])
df['non_check'] = np.where(df['รหัส (สินค้าย่อย)'].str.find("ใบกำกับ") == 0, True, df['non_check'])

for i in range(3585, 3631):
    df['non_check'] = np.where(df['รหัส (สินค้าย่อย)'].str.find(chr(i)) == 0, True, df['non_check'])

non_check_count = df['non_check'].sum()
check_count = len(df) - non_check_count

#check เกิน 7.30*3 ไหม
all = check_count * 3.33
nonall = non_check_count * 2

alltime = all + nonall
print(alltime)

#นับจำนวณซองของแต่ละคน
df.insert(13, 'จำนวนออเดอร์แต่ละคน', '', True)

#เริมแยกคน
if (time_min < alltime): #กรณีออเดอร์มากกว่าจำนวณชั่วโมงที่จะให้ทำ
  time_one = time_min / 3
  ontime1 = 0
  ontime2 = 0
  ontime3 = 0
  check1 = 1
  check2 = 0
  check3 = 0
  i = 0
  print(time_one)
  #first
  while ontime1 <= time_one:
    if i != 0 and df['เลขที่ออเดอร์ (ออเดอร์)'][i] != df['เลขที่ออเดอร์ (ออเดอร์)'][i-1]:
      check1 += 1
    if df['non_check'][i] == True:
      df['คนแพค'][i] = 2
      ontime1 += (2 * int(df['จำนวนที่ซื้อ'][i]))
      i = i + 1
    else:
      df['คนแพค'][i] = 1
      ontime1 += (3.33 * int(df['จำนวนที่ซื้อ'][i]))
      i = i + 1
  #second
  while ontime2 <= time_one:
    if df['เลขที่ออเดอร์ (ออเดอร์)'][i] != df['เลขที่ออเดอร์ (ออเดอร์)'][i-1]:
      check2 += 1
    if df['non_check'][i] == True:
      df['คนแพค'][i] = 4
      ontime2 += (2 * int(df['จำนวนที่ซื้อ'][i]))
      i = i + 1
    else:
      df['คนแพค'][i] = 3
      ontime2 += (3.33 * int(df['จำนวนที่ซื้อ'][i]))
      i = i + 1
  #second
  while ontime3 <=  time_one:
    if df['เลขที่ออเดอร์ (ออเดอร์)'][i] != df['เลขที่ออเดอร์ (ออเดอร์)'][i-1]:
      check3 += 1
    if df['non_check'][i] == True:
      df['คนแพค'][i] = 6
      ontime3 += (2 * int(df['จำนวนที่ซื้อ'][i]))
      i = i + 1
    else:
      df['คนแพค'][i] = 5
      ontime3 += (3.33 * int(df['จำนวนที่ซื้อ'][i]))
      i = i + 1
else:
  time_one = alltime / 3
  ontime1 = 0
  ontime2 = 0
  ontime3 = 0
  check1 = 1
  check2 = 0
  check3 = 0
  i = 0
  print(time_one)
  #first
  while ontime1 < time_one:
    if i != 0 and df['เลขที่ออเดอร์ (ออเดอร์)'][i] != df['เลขที่ออเดอร์ (ออเดอร์)'][i-1]:
      check1 += 1
    if df['non_check'][i] == True:
      df['คนแพค'][i] = 2
      ontime1 += (2 * int(df['จำนวนที่ซื้อ'][i]))
      i = i + 1
    else:
      df['คนแพค'][i] = 1
      ontime1 += (3.33 * int(df['จำนวนที่ซื้อ'][i]))
      i = i + 1
  print(F'ontime1 = {ontime1} i = {i}')
  #second
  while ontime2 < time_one:
    if df['เลขที่ออเดอร์ (ออเดอร์)'][i] != df['เลขที่ออเดอร์ (ออเดอร์)'][i-1]:
      check2 += 1
    if df['non_check'][i] == True:
      df['คนแพค'][i] = 4
      ontime2 += (2 * int(df['จำนวนที่ซื้อ'][i]))
      i = i + 1
    else:
      df['คนแพค'][i] = 3
      ontime2 += (3.33 * int(df['จำนวนที่ซื้อ'][i]))
      i = i + 1
  #second
  while i <  len(df):
    if df['เลขที่ออเดอร์ (ออเดอร์)'][i] != df['เลขที่ออเดอร์ (ออเดอร์)'][i-1]:
      check3 += 1
    if df['non_check'][i] == True:
      df['คนแพค'][i] = 6
      ontime3 += (2 * int(df['จำนวนที่ซื้อ'][i]))
      i = i + 1
    else:
      df['คนแพค'][i] = 5
      ontime3 += (3.33 * int(df['จำนวนที่ซื้อ'][i]))
      i = i + 1

#แสดงออเดอร์แต่ละคน
df['จำนวนออเดอร์แต่ละคน'][1] = 'เอื้อ (1,2)'
df['จำนวนออเดอร์แต่ละคน'][2] = check1
df['จำนวนออเดอร์แต่ละคน'][3] = F'เวลา{ontime1/60}'

df['จำนวนออเดอร์แต่ละคน'][4] = 'ฟ้า (3,4)'
df['จำนวนออเดอร์แต่ละคน'][5] = check2
df['จำนวนออเดอร์แต่ละคน'][6] = F'เวลา{ontime2/60}'

df['จำนวนออเดอร์แต่ละคน'][7] = 'เก้า (5,6)'
df['จำนวนออเดอร์แต่ละคน'][8] = check3
df['จำนวนออเดอร์แต่ละคน'][9] = F'เวลา{ontime3/60}'

df = df.drop('non_check', 1)
df.to_excel(r'Export.xlsx', index = False)