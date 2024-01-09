Validates python input.

Usage:

```python
from Validizier import Validate as V
# Imports the validate class as V

while True:
  Error, Num = V.number(input("Enter a whole number between 1-4: "), "int", "1-4")
  # Uses optional arguments 'return_type' and 'num_range'
  # Return type can equal "int", "float", "$" or, "cash" ("$" and "cash" are the same) if you dont provide a return type or
  # if the return type is invalid it will return whatever was inputed. I.E if they input "2.2" you'll get 2.2.
  if Error:
    print(Num)
  else:
    break
  
```

Optionally the class can automate inputs:

```python
from Validizier import Validate as V
# Imports the validate class as V

Num = V(V.number, "Enter a number between 1-4: ", "int", "1-4")
# Auto loops with the first being the input type, the second being the input prompt, and the third being the arguments in order.
print(v.V) # Processed value i.e 3
print(v.UP) # Unprocessed value i.e '3'
print(v.T) # Value type i.e 'number'
  
```

I only kept the non-autmoated because the autmoated uses that and i'd have to recode plus if you do it manually you can
customize the outputs.
