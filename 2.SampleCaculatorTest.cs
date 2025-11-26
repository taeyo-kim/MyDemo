using Xunit;
using System;

// SimpleCalculator 클래스에 대한 단위 테스트
public class SimpleCalculatorTest
{
    private readonly SimpleCalculator _calculator;

    public SimpleCalculatorTest()
    {
        _calculator = new SimpleCalculator();
    }

    // Add 메서드 테스트 - 양수 더하기
    [Fact]
    public void Add_PositiveNumbers_ReturnsCorrectSum()
    {
        // Arrange
        int a = 5;
        int b = 3;

        // Act
        int result = _calculator.Add(a, b);

        // Assert
        Assert.Equal(8, result);
    }

    // Add 메서드 테스트 - 음수 더하기
    [Fact]
    public void Add_NegativeNumbers_ReturnsCorrectSum()
    {
        // Arrange
        int a = -5;
        int b = -3;

        // Act
        int result = _calculator.Add(a, b);

        // Assert
        Assert.Equal(-8, result);
    }

    // Subtract 메서드 테스트 - 양수 빼기
    [Fact]
    public void Subtract_PositiveNumbers_ReturnsCorrectDifference()
    {
        // Arrange
        int a = 10;
        int b = 4;

        // Act
        int result = _calculator.Subtract(a, b);

        // Assert
        Assert.Equal(6, result);
    }

    // Subtract 메서드 테스트 - 음수 결과
    [Fact]
    public void Subtract_ResultIsNegative_ReturnsCorrectDifference()
    {
        // Arrange
        int a = 3;
        int b = 7;

        // Act
        int result = _calculator.Subtract(a, b);

        // Assert
        Assert.Equal(-4, result);
    }

    // Multiply 메서드 테스트 - 양수 곱하기
    [Fact]
    public void Multiply_PositiveNumbers_ReturnsCorrectProduct()
    {
        // Arrange
        int a = 6;
        int b = 7;

        // Act
        int result = _calculator.Multiply(a, b);

        // Assert
        Assert.Equal(42, result);
    }

    // Multiply 메서드 테스트 - 0 곱하기
    [Fact]
    public void Multiply_WithZero_ReturnsZero()
    {
        // Arrange
        int a = 5;
        int b = 0;

        // Act
        int result = _calculator.Multiply(a, b);

        // Assert
        Assert.Equal(0, result);
    }

    // Divide 메서드 테스트 - 정상적인 나누기
    [Fact]
    public void Divide_ValidNumbers_ReturnsCorrectQuotient()
    {
        // Arrange
        int a = 10;
        int b = 2;

        // Act
        double result = _calculator.Divide(a, b);

        // Assert
        Assert.Equal(5.0, result);
    }

    // Divide 메서드 테스트 - 소수점 결과
    [Fact]
    public void Divide_ResultIsDecimal_ReturnsCorrectQuotient()
    {
        // Arrange
        int a = 10;
        int b = 3;

        // Act
        double result = _calculator.Divide(a, b);

        // Assert
        Assert.Equal(3.333333, result, 5);
    }

    // Divide 메서드 테스트 - 0으로 나누기 예외
    [Fact]
    public void Divide_ByZero_ThrowsDivideByZeroException()
    {
        // Arrange
        int a = 10;
        int b = 0;

        // Act & Assert
        Assert.Throws<DivideByZeroException>(() => _calculator.Divide(a, b));
    }

    // Divide 메서드 테스트 - 0으로 나누기 예외 메시지 확인
    [Fact]
    public void Divide_ByZero_ThrowsExceptionWithCorrectMessage()
    {
        // Arrange
        int a = 10;
        int b = 0;

        // Act & Assert
        var exception = Assert.Throws<DivideByZeroException>(() => _calculator.Divide(a, b));
        Assert.Equal("0으로 나눌 수 없습니다.", exception.Message);
    }
}