# Writing specs with sure

## Python files

Sure provides a simple DSL for writing specifications.

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
use [3rd party libraries](/sure/with/nose/py.test/should_dsl) but sure
itself is an assertion library that
[leverages fluency and expressivity](/path/to/sure expectations
documentation).

## Predicates

Sometimes it might be useful to execute python code that will
instantiate classes, prepare data fixtures or even spin up his own
http server serving fake data.

Before running the assertions, the developer might want to execute
code that will instantiate classes, prepare data fixtures or even spin
up his own http server serving fake data.

In order to leverage this, sure also looks for python callables (just
like it does for ["specifications"](./ref/to/specifications)) although
they are defined with a different syntax.

This can be achieved through "predicates". Predicates are also python
callables, but they are defined with a different prefix:
`ensuring_`. The underscore is also optional in this case, and its
code is executed before each specification. Many predicates might be
defined per python file, they are executed in the same order they were
declared.

Examples:

```python
def ensuring_some_class():
    u"The class Foobar"


def ensure_it_has_a_method_that_prints():
    "its method '.uppercase(string)' takes a string and makes it supercased"

    FooBar.uppercase("whatever").should.equal("WHATEVER")
```

# TODO:

Write about teardown, come out with a term that suits its counterpart
"predicate".


# Spec mocks

    return_value = module_being_tested.some_method(spec.mock.sys)

    return_value.should.equal("expected value")

    spec.mock.sys
