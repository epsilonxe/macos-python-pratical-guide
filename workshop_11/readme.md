# Workshop 11

จงเขียนโปรแกรมเพื่อศึกษาแบบจำลองทางคณิตศาสตร์สำหรับการแพร่ระบาดของเชื้อโรคต่อไปนี้

```
S_{n+1} = S{n} - beta * I_{n} * S_{n} + gamma * R_{n}
I_{n+1} = I{n} + beta * I_{n} * S_{n} - delta * I_{n}
R_{n+1} = R{N} + delta * I_{n} - gamma * R_{n}
```

เมื่อ 
* S_n คือ จำนวนของผู้ที่เป็นกลุ่มเสี่ยงในวันที่ n
* I_n คือ จำนวนของผู้ที่ติดเชื้อในวันที่ n
* R_n คือ จำนวนของผู้ที่รักษาหาย (และมีภูมิคุ้มกัน) ในวันที่ n

โดยมีพารามิเตอร์ของแบบจำลอง ดังนี้
* beta คือ อัตราการแพร่ระบาดของเชื้อ
* delta คือ อัตราการรักษา
* gamma คือ อัตราการลดลงของภูมิคุ้มกัน


## Example
```
Disease Spreading Model
- - - - - - - - - - - - -
Initial Variables
Enter the number of S(0): 60
Enter the number of I(0): 0.0001
Enter the number of R(0): 0
- - - - - - - - - - - - -
Parameters
Enter the number of beta: 0.00045
Enter the number of delta: 0.0025
Enter the number of gamma: 0.00002
- - - - - - - - - - - - -
Enter the number of days: 365
Here is the results
S = [60, 59.445, 58.4343, ..., 0.98234]
I = [0.0001, 0.000145, 0.00034, ..., 0.00445 ]
R = [0.0, 0.000145, 0.00034, ..., 0.45640 ]
```