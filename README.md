I developed a function in python that would detect important areas in the last 6 months where the price bounced back or the price could not keep going up (peaks). These are the famous support and resistance areas. 
I developed this function to be aware of these areas that could have high liquidity, the price might react in these areas. (OLD MESSY CODE) 
I played around with this function, inside the loop I coded a logic where the system would be aware of when the price is very close to these areas and try to detect trading signals in these areas by cheking 
if the price would break these areas (BREAKOUT) or reject these areas aggressively with marubozu candles. For instance, in the file main.py I had this parameter, the marubozu candles and also I played with their size. 
I also played around with different timeframes 4hrs candles, 1hrs candles and daily candles...
Here there is a screen shot of what happens behind the scenes behind these lines of code:
![Texto (1)](https://github.com/user-attachments/assets/bd69c6b7-3c8a-4b94-ae0c-993e8f7578c8)
