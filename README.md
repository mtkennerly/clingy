# Clingy
Clingy lets you save attachments from plain text emails.

From the command line, you can use it like this:

```
clingy email1.txt email2.txt email3.txt
```

By default, the attachments will be saved into the current directory.
You can specify a different directory using `-d` or `--directory` like so,
and the directory will be created if it does not exist:

```
clingy email.txt -d out
```

You can save specific attachments using glob patterns (`-g` or `--glob`)
and regular expressions (`-r` or `--regex`):

```
clingy email.txt -g "*.txt"
clingy email.txt -r "^.+\.txt$"
```

When you `pip install clingy`, Python will create a platform-appropriate
executable in the Python Scripts directory. Assuming you have that directory
in your path, you can just run `clingy` from the console.

You can also use it as a library:

```python
import clingy

# List all attachments from an email file
clingy.find("email.txt")

# List all attachments from an email string
with open("email.txt") as file:
    clingy.find(file.read())

# Save all attachments by filename
clingy.save("email.txt")

# Save all attachments by string
with open("email.txt") as file:
    clingy.save(file.read())

# Save single attachment from email.message.Message object
attachments = clingy.find("email.txt")
clingy.save(attachments[0])

# Find all TXT files via glob pattern:
clingy.find("email.txt", glob="*.txt")

# Save all TXT files via regular expression:
clingy.save("email.txt", regex=r"^.+\.txt$")
```

The combo glob/regex matcher is also available for good measure:

```python
import clingy

clingy.match("foo.txt", glob="*.txt")
clingy.match("foo.txt", regex="\.txt$")
````
