



def intToRoman(num):
    """
    :type num: int
    :rtype: str
    """
    
    values = [ 1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1 ]
    numerals = [ "M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I" ]
    res= ''
    for n , v in zip(numerals, values): 
        res += (num//v) * n
        num %= v 
    return res          





    
num=3 
print(intToRoman(num))