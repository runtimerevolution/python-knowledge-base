# Code Principles

Code should be clear and easy to maintain, by maintaining we also mean writing and
revisiting tests if necessary. Below there's a list of principles which used
with [The Zen of Python](zen_of_python.md), will help us to write better code as well as to test it.

## KISS - Keep it simple, stupid [^1]

The snippet below is hard to read and takes time to understand

```python
f = lambda x: x if x in {0, 1} else f(x - 1) + f(x - 2)
```

Alternatively, the next code snippet is much easier to understand and maintain. 

```python
def fibonacci(number: int) -> int:
    if number in {0, 1}:
        return number
    return fibonacci(number - 1) + fibonacci(number - 2)
```

By adding descriptive names, type hints, and splitting the line into multiple ones it gets
easier to read and maintain. 

> The main goal in design should always be to be as easy to understand
as possible.

## DRY - Don't repeat yourself [^2]

This principle is about writing functions and automating sections of code that are repeated. If you perform the same
task multiple times in your code, consider a function or a loop to make your workflow more efficient.

Let's consider the next example where we'll be using a math expression to convert temperature values from fahrenheit 
to celsius.

```python
temp_1 = 32
res_1 = (temp_1-32) * 5/9

temp_2 = 40
res_2 = (temp_2-32) * 5/9
```

Some points to consider:

- If the calculation changes, we'd need to update both expressions
- it's not clear what the math expression is calculating, unless you're familiar with it

Let's create a method for the math expression.

```python
def conv_fahr_to_celsius(fahr: float) -> float:
    """Convert temperature in Fahrenheit to Celsius.

    Parameters:
    -----------
    fahr: float
        The temperature in Fahrenheit.
    
    Returns:
    -----------
    Celsius : int or float
        The temperature in Celsius.
    """
    celsius = (fahr-32) * 5/9
    return celsius
```

And update the previous sample to use this method.

```python
fahr_1 = 32
celsius_1 = conv_fahr_to_celsius(fahr_1)

fahr_2 = 40
celsius_2 = conv_fahr_to_celsius(fahr_2)
```

In summary

- The code is cleaner, because the repeated calculation was replaced with a function
- If this function is well-defined with a docstring that describes what it does, it is easier to
both understand and use. 
- If you need to change the calculation itself, you can do so once in the function

## SoC - Separation of concerns [^1]

A known example of this is the model-view-controller (MVC) design. MVC separates a program
into three distinct areas: the data (model), the logic (controller), and what the page displays (view).

## SOLID [^3]

SOLID is a mnemonic acronym for five design principles intended to make software designs more understandable, flexible,
and maintainable.

- **S**ingle-responsibility principle: _"A class should have one, and only one, reason to change."_
- **O**pen–closed principle: _"Entities should be open for extension, but closed for modification."_
- **L**iskov substitution principle: _"Functions that use pointers or references to base classes must be able to use objects of derived classes without knowing it."_
- **I**nterface segregation principle: _"A client should not be forced to implement an interface that it doesn’t use."_
- **D**ependency inversion principle: _"Depend upon abstractions, not concretions."_


### Single-responsibility principle (SRP)

Every component of your code (in general a class, but also a function) should have one and only one responsibility.
As a consequence of that, there should be only a reason to change it.

Too often you see a piece of code that takes care of an entire process all at once. I.e., A function that loads data,
modifies and, plots them, all before returning its result.

Let’s take a simpler example, where we have a list of number L = [n1, n2, …, nx] and we compute some mathematical
functions to this list. For example, compute the mean, median, etc.

A **bad approach** would be to have a single function doing all the work:

```python
import numpy as np

def math_operations(list_):
    # Compute Average
    print(f"the mean is {np.mean(list_)}")
    # Compute Max
    print(f"the max is {np.max(list_)}") 

math_operations(list_ = [1,2,3,4,5])
# the mean is 3.0
# the max is 5
```

The first thing we should do, to make this more SRP compliant, is to split the function math_operations into atomic
functions! Thus, when a function’s responsibility cannot be divided into more sub-parts.

The second step is to make a single function (or class), generically named, “main”. This will call all the other
functions one-by-one in a step-to-step process.

```python
import numpy as np

def get_mean(list_):
    """
        Compute Mean
    """
    print(f"the mean is {np.mean(list_)}") 

def get_max(list_):
    """
        Compute Max
    """
    print(f"the max is {np.max(list_)}") 

def main(list_): 
    # Compute Average
    get_mean(list_)
    # Compute Max
    get_max(list_)

main([1,2,3,4,5])
# the mean is 3.0
# the max is 5
```

Now, you would only have one single reason to change each function connected with “main”.

The result of this simple action is that now:

1. It is easier to localize errors. Any error in execution will point out to a smaller section of your code,
accelerating your debug phase.
2. Any part of the code is reusable in other section of your code.
3. Moreover and, often overlooked, is that it is easier to create testing for each function of your code.
Side note on testing: You should write tests before you actually write the script. But, this is often ignored in
favour of creating some nice result to be shown to the stakeholders instead.

This is already a much bigger improvement with respect to the first code example. But, having created a “main” and
calling functions with single responsibility is not the full fulfilment of the SR principle. Indeed, our “main” has
many reasons to be changed. The class is actually fragile and hard to maintain. To solve that, let’s introduce the
next principle.

### Open/Closed principle (OCP)

You should not need to modify the code you have already written to accommodate new functionality, but simply add what
you now need.

This does not mean that you cannot change your code when the code premises needs to be modified, but that if you need
to add new functions similar to the one present, you should not require to change other parts of the code. To clarify
this point let’s refer to the example we saw earlier. If we wanted to add new functionality, for example, compute the
median, we should have created a new method function and add its invocation to “main”. That would have added an
extension but also modified the main.

We can solve this by turning all the functions we wrote into subclasses of a class. In this case, I have created an
abstract class called “Operations” with an abstract method “get_operation”. (Abstract classes are generally an
advanced topic. If you don’t know what an abstract class is, you can run the following code even without).

Now, all the old functions, now classes are called by the __subclasses__() method. That will find all classes inheriting
from Operations and operate the function “operations” that is present in all subclasses.

> for additional information on abstractmethod decorator please
> check https://docs.python.org/3/library/abc.html#abc.abstractmethod

```python
import numpy as np
from abc import ABC, abstractmethod

class Operations(ABC):
    """Operations"""
    @staticmethod
    @abstractmethod
    def operation(list_):
        pass

class Mean(Operations):
    """Compute Max"""
    @staticmethod
    def operation(list_):
        print(f"The mean is {np.mean(list_)}")

class Max(Operations):
    """Compute Max"""
    @staticmethod
    def operation(list_):
        print(f"The max is {np.max(list_)}")

class Main:
    """Main"""
    @staticmethod
    @abstractmethod
    def get_operations(list_):
        # __subclasses__ will find all classes inheriting from Operations
        for operation in Operations.__subclasses__():
            operation.operation(list_)


if __name__ == "__main__":
    Main.get_operations([1,2,3,4,5])
# The mean is 3.0
# The max is 5
```

If now we want to add a new operation e.g.: median, we will only need to add a class “Median” inheriting from the class
“Operations”. The newly formed subclass will be immediately picked up by __subclasses__() and no modification in any
other part of the code needs to happen.

The result is a very flexible class, that requires minimum time to be maintained.

### The Liskov substitution principle (LSP)

Functions that use pointers or references to base classes must be able to use objects of derived classes without
knowing it, that alternatively can be expressed as, derived classes must be substitutable for their base classes.

In (maybe) simpler words, if a subclass redefines a function also present in the parent class, a client-user should not
be noticing any difference in behaviour, and it is a substitute for the base class. For example, if you are using a
function and your colleague change the base class, you should not notice any difference in the function that you are
using.

Among all the SOLID principle, this is the most abstruse to understand and to explain. For this principle, there is no
standard “template-like” solution where it must be applied, and it is hard to offer a “standard example” to showcase.

In the most simplistic way, I can put it, this principle can be summarised by saying:
If in a subclass, you redefine a function that is also present in the base class, the two functions ought to have the
same behaviour. This, though, does not mean that they must be mandatory equal, but that the user, should expect that
the same type of result, given the same input.
In the example ocp.py, the “operation” method is present in the subclasses and in the base class, and an end-user should
expect the same behaviour from the two.

The result of this principle is that we’d write our code in a consistent manner and, the end-user will need to learn how
our code works, only one.


>A consequence of LSP is that: the new redefined function in the subclass should be valid and
>be possibly used wherever the same function in the parent class is used.
>
>This is not, typically the case, indeed usually we, human, think in terms of set theory.
>Having a class that define a concept and subclasses that expand the first with an
>exception or different behaviour.
>
>For example, the subclass “Platypus”, of the base class “Mammals”, would have the
>exception that these mammals lay eggs. The LSP, tell us that it would create a
>function called “give_birth”, this function will have different behaviour
>for the subclass Platypus and the subclass Dog. Therefore, we should have had a
>more abstract base class than Mammals that accommodate this.
>If this sounds very confusing, do not worry, the application of this latter aspect
>of the LSP is rarely fully implemented, and it rarely leaves the theoretical textbooks.

### The Interface Segregation Principle (ISP)

Many client-specific interfaces are better than one general-purpose interface. In the context of classes, an interface
is considered, all the methods and properties exposed, thus, everything that a user can interact with that belongs to
that class.

In this sense, the IS principles tell us that a class should only have the interface needed (SRP) and avoid methods
that won’t work or that have no reason to be part of that class.

This problem arises, primarily, when, a subclass inherits methods from a base class that it does not need.

Let’s see an example:

> for additional information on abstractmethod decorator please
> check https://docs.python.org/3/library/abc.html#abc.abstractmethod

```python
from abc import ABC, abstractmethod

class Mammals(ABC):
    @staticmethod
    @abstractmethod
    def swim():
        print("Can Swim")

    @staticmethod
    @abstractmethod
    def walk():
        print("Can Walk")

class Human(Mammals):
    @staticmethod
    def swim():
        return print("Humans can swim")

    @staticmethod
    def walk():
        return print("Humans can walk")

class Whale(Mammals):
    @staticmethod
    def swim():
        return print("Whales can swim") 
```

For this example, we have got the abstract class “Mammals” that has two abstract methods: “walk” and “swim”. These two
elements will belong to the subclass “Human”, whereas only “swim” will belong to the subclass “Whale”.

And indeed, if we run this code we could have:

```python
Human.swim()
Human.walk()

Whale.swim()
Whale.walk()

# Humans can swim
# Humans can walk
# Whales can swim
# Can Walk
```

The subclass whale can still invoke the method “walk” but it shouldn’t, and we must avoid it.

The way suggested by ISP is to create more client-specific interfaces rather than one general-purpose interface.
So, our code example becomes:

```python
from abc import ABC, abstractmethod

class Walker(ABC):
    @staticmethod
    @abstractmethod
    def walk():
        return print("Can Walk")

class Swimmer(ABC):
    @staticmethod
    @abstractmethod
    def swim():
        return print("Can Swim")

class Human(Walker, Swimmer):
    @staticmethod
    def walk():
        return print("Humans can walk")
    @staticmethod
    def swim():
        return print("Humans can swim")

class Whale(Swimmer):
    @staticmethod
    def swim():
        return print("Whales can swim") 

if __name__ == "__main__":
  Human.walk()
  Human.swim()

  Whale.swim()
  Whale.walk()

# Humans can walk
# Humans can swim
# Whales can swim
# AttributeError: type object 'Whale' has no attribute 'walk'
```

Now, every subclass inherits only what it needs, avoiding invoking an out-of-context (wrong) sub-method. That might
create an error hard to catch.

This principle is closely connected with the other ones and specifically, it tells us to keep the content of a subclass
clean from elements of no use to that subclass. This has the final aim to keep our classes clean and minimise mistakes.

### Dependency Inversion Principle (DIP)

Abstractions should not depend on details. Details should depend on abstraction. High-level modules should not depend
on low-level modules. Both should depend on abstractions. So, that abstractions (e.g., the interface, as seen above)
should not be dependent on low-level methods but both should depend on a third interface.

To better explain this concept, I prefer to think of a sort of information flow.

Imagine that you have a program that takes in input a specific set of info (a file, a format, etc) and you wrote a
script to process it. What would happen if that info were subject to change?
You would have to rewrite your script and adjust the new format. Losing the retro compatibility with the older files.

However, you could solve this by creating a third abstraction that takes the info as input and passes it to the others.
This is basically what an API is also, used for.

``` mermaid
flowchart LR
    ObjectA --> |references| ObjectB
    subgraph Package B
    ObjectB
    end
    subgraph Package A
    ObjectA
    end
```

``` mermaid
flowchart TB
    ObjectB --> |inherits| Interface
    subgraph Package B
    ObjectB
    end
    subgraph Package A
    ObjectA--> |references| Interface
    end
```

The interesting design concept of this principle is that it is the reverse approach to what we would normally do.

With the DIP in mind, we would start from the end of the project, in which our code is independent of what takes in
input, and it is not susceptible to changes and out of our direct control.

## YAGNI - You ain't gonna need it

It's a mantra from Extreme Programming that's often used generally in agile software teams. It's a statement that some
capability we presume our software needs in the future should not be built now because "you aren't gonna need it". 

> For additional information on this make sure to
> check [https://www.martinfowler.com/bliki/Yagni.html](https://www.martinfowler.com/bliki/Yagni.html)

## Document your code

1. Don't comment bad code, rewrite it
2. Readable code doesn't need comments
3. Don't add noise comments

[^1]: https://testdriven.io/blog/clean-code-python/
[^2]: https://www.earthdatascience.org/courses/intro-to-earth-data-science/write-efficient-python-code/intro-to-clean-code/dry-modular-code/
[^3]: https://towardsdatascience.com/solid-coding-in-python-1281392a6a94
