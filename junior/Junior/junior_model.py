
stack = []

def push_into_stack(item):
   global stack
   stack.append(item)
   return f"pushed {item}"

def pop():
   global stack
   stack = stack[0:-1]

def get_stack():
   global stack
   return stack

