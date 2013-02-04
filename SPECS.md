# Writing specs with sure

Sure comes with its own [DSL](http://en.wikipedia.org/wiki/Domain-specific_language) for writing tests in python.

Its main goal is to leverage fluency and expressivity while writing
automated tests in the python programming language.

Sure enforces some software engineering techniques to make the
destination code more decoupled and clean. Mostly through testing
small units of logic.

It is known that code written through TDD can be a lot cleaner and
more robust when covered with unit tests. Sure is an attempt to make
writing unit tests a more pleasant experience for python developers.

In sure tests tests are referred as "specifications" or "spec", and it
is grouped in "suites" that are surrounded by actions taken before and/or
after a set of tests (predicates and complements).

Each specification is meant to test one single behavior unit. "Sure"
is simply a python library so a developer could circunvent its
proposed practices, but it's important to reinforce that a developer
that is using sure to write its tests should be concerned about
writing decoupled code, and therefore writing a single test per
behavior unit is important.



## Python files

Although sure is a
[DSL](http://en.wikipedia.org/wiki/Domain-specific_language), it's
nothing but just python code. Sure will work with any python above
version 2.6 but it works better with the default implementation
[CPython](http://en.wikipedia.org/wiki/CPython).

## Specifications

Tests are called "specifications".

Specifications are simple python callables (functions, methods or even
"`__call__`ed" classes) which are sensitive to `AssertionError`
exceptions performed during expectations.

They can be defined with the prefix `ensure_`. The underscore
character is optional and the word is matched without case
sensitivity.

It leaves room for some level of flexibility and
expressivity like in the following examples:

```python
def ensure_one_behavior_unit(spec):
    ("it behaves in a certain way if a parameter matches certain condition")
    # perform expectations here


class EnsureAFewBehaviorUnits(sure.Spec):

    def ensure_one_behavior_unit(self):
        ("Same as below but now with multiple lines so that neither PEP8 "
         "or your test's expressivity get hurt")

    def ensure_another_behavior(self):
        u"Last one in order, now with unicode characters \u2665"
```

Expectations nothing but python calls that will raise `AssertionError`
exceptions, it could be achieved by simple making `assert` calls or
use [3rd party libraries](SPECS.md#3rd-party-libraries) but sure
itself is an assertion library that
[leverages fluency and expressivity](SPECS.md#expectations).

## Predicates

Sometimes it might be useful to execute arbitrary python code before
running specifications along with its expectations. Maybe classes must
be instantiated, or a data store must be prepared, data fixtures setup
or even something more laborated like spinning up a http server that
will serve fake data.

In order to leverage this, sure also looks for python callables (just
like it does for ["specifications"](./ref/to/specifications)) although
they are defined with a different syntax.

This can be achieved through "predicates". Predicates are also python
callables, but they are defined with a different prefix:
`ensuring_`. The underscore is also optional in this case, and its
code is executed before each specification. Many predicates might be
defined per python file, they are executed in the same order they were
declared.

### Examples:

```python
def ensuring_some_class(spec):
    u"The class Foobar"
    spec.foobar = FooBar()


def ensure_it_has_a_method_that_prints(spec):
    "its method '.uppercase(string)' takes a string and makes it supercased"

    FooBar.uppercase("whatever").should.equal("WHATEVER")
    spec.foobar.uppercase("foo").should.equal("FOO")
```

## Complements

If in one hand predicates leverage setting up a test environment, its
counterpart "complement" help on taking actions after each spec.

A complement can be defined with the syntax `finally_`, the underscore
is also optional here.

### Examples:

```python
def ensuring_some_class(spec):
    u"The class Foobar"
    spec.foobar = Foobar()

def ensure_it_has_a_method_that_prints(spec):
    "its method '.uppercase(string)' takes a string and makes it supercased"
    spec.foobar.uppercase("foo").should.equal("FOO")

def finally_clean_up_the_unecessary_memory(spec):
    "Cleaning up unecessary instances"

    del spec.foobar
```

# Spec mocks (todo)...

    return_value = module_being_tested.some_method(spec.mock.sys)

    return_value.should.equal("expected value")

    spec.mock.sys
