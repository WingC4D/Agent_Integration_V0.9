from pkg.calculator import Calculator;
from pkg.render import render;
import sys;
def main():
    calculator = Calculator();
    if (len(sys.argv) <= 1):
        print('Calculator App\nUsage: python main.py "<expression>"\nExample: python main.py "3 + 5"');
        return;
    
    expression: str | int | float = " ".join(sys.argv[1:]);
    try:
        result: int | float = calculator.evaluate(expression);
        to_print: str = render(expression, result);
        print(to_print);
        
    except Exception as e:
        print(f"Error: {e}");
        
        
if __name__ == "__main__":
     main()