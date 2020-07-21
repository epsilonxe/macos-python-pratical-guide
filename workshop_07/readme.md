# Workshop 07

จงเขียนเกมที่ให้ผู้เล่นเดาตัวเลขจำนวนเต็ม 1-100 
ที่ถูกกำหนดไว้ล่วงหน้าแล้ว โดยที่

1. เลขที่ถูกกำหนดไว้นั้นจะต้องถูกสุ่มขึ้น
1. ถ้าผู้เล่นเดาถูก เกมจะจบลง
1. ถ้าผู้เล่นเดาผิด จะต้องบอกว่า เลขดังกล่าวนั้นมากไปหรือน้อยไปจากตัวเลขที่กำหนดไว้
1. ถ้าผู้เล่นเดาผิด จะต้องเล่นเกมนี้ต่อไป
1. ผู้เล่นสามารถหยุดเกมโดยพิมพ์ว่า give_up เกมจะเฉลยเลขที่ถูกต้องและเกมจะจบลง

## Example
```
Gussing my number (1-100)
Your guess is: 78
No, it is not. It is too high.
Your guess is: 50
No, it is not. It is too low.
Your guess is: 63
No, it is not. It is too low.
Your guess is: give_up
Sorry loser. The correct one is 65.
```
