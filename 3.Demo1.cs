using System;

namespace Demo1
{
    //소수 판별 함수 구현
    public class PrimeChecker
    {
        public bool IsPrime(int number)
        {
            if (number <= 1) return false;
            for (int i = 2; i <= Math.Sqrt(number); i++)
            {
                if (number % i == 0) return false;
            }
            return true;
        }
    }

    
    

}
