# Programming Conventions
This project strictly follows all recommendations made by the PEP-8. However,
there are some additional ones described here in order to maintain enough
consistency to achieve duck typing and similar concepts.

> "If it walks like a duck and it quacks like a duck, it must be a duck".

## Naming
As specified by PEP-8, variables, functions and methods should be named in
lowercase with words separated by underscores like this:
`some_funny_function(instance.an_epic_method(variable_with_a_value))`

However, if the name only consists of two words, the underscore is omitted
as follows:
`somefunc(instance.callmeth(thevar))`

Words should also be abbreviated in the second case to improve readability;
otherwise, don't abbreviate words or sentences:
```python
im_an_example_of_a_directory = "/im/not/abbreviated/and/thats/okay"
im_ex_ofdir = "/not/const/hrdr/2/read"
simpledir = "/much/better"
```

## Importing
**Never** use star imports (`from package import *`), even for local packages
they make debugging *considerably* harder and the probability of having
conflicting object names dramatically increases (if not *appears*).

Direct imports (`from package import object`) are only allowed if the
object in question becomes too repetitive in the code. Otherwise, having
verbose code is better than inner conflicts and misleading names.

In case the object's name conflicts with a built-in or a local one, always
import its package with its path as usual (`import some.package`).

## Magic functions, methods and variables
Always keep \_\_init\_\_.py files empty.
The \_\_repr\_\_ and \_\_str\_\_ methods should be *exactly* the same.
Don't use the \_\_doc\_\_ method, just type a multiline string at the start
of the method instead.
`if __name__ == "__main__": ...` statements should *not* be interactive, but
rather initialize previously programmed tests. However, they should include
a warning and ask for a confirmation to make sure the user doesn't
accidentally run debugging tests.

## Strings
Despite Python supporting UTF-8 encoding by default, to avoid possible errors
with older machines and generally following the standards; do not use
non-ASCII characters for variables, functions, packages, classes, methods and
filenames. They're allowed on everything else as long as you're sure it's not
something crucial that can be potentially broken by them.

Double quotes ("") are generally preferred over single quotes ('') unless the
string itself has them; if the string has both (for some reason), use double
quotes and escape the rest with a backslash (\\).

The preferred formatting method is the f notation at the start of strings
(`f"some {'string'}"`). If it's not possible to use it in a certain case, use
the str.format method (`"another {}".format("string")`), and if it cannot be
used either for backwards compatibility use the old % formatting
(`"yet another %s" % ("string")`).
Joining (`"".join(["yet ", "another ", "string"])`) should be used for cases
were none of the previously mentioned methods work or it's more understandable.
For paths, always use the join function from the os.path module.

Concatenation should never be used instead of the previously mentioned methods
unless it's an *extreme* case; however, it is actually encouraged for strings
that are too long to fit in a single line and combining 2 of them:
```python
class OhNo:
    def method(self):
        try:
            ...
        except:
            for i in something:
                print("As you can see, this is a very long line that's about "
                      "to exceed 79 characters. Thankfully, we have Python's "
                      "automatic string concatenation!")

foo = foo + bar  # This is good too!
```

*Copyright (C) Suaj, 2021*
