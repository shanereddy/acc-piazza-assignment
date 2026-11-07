# Development Log
## Milestone 1: Initial setup
### 25/10/2026
I have created the repository in Github, with a skeleton folder structure and initial python packages and files used in class 3 as a foundation for this application.

Empty placeholder files are created in the folders as empty folders are ignored by `git`. These will be removed once the application files are created.

Sources: [CC Lab (class 3)](https://github.com/warestack/cc/tree/main/class-3/lab)
```
Commit Links: None
```
## Milestone 2: Application Development
### 01/11/2026
I've added the health check as a router to keep the routes tidy.

I have added an `active` column on the User table so that a user may be deactivated. This will influence login, as we won't allow a deactivated user to be logged in. I was careful not to add this to registration as we want to check all rows in our database for an already registered user.

Sources: [CC Lab (class 4)](https://github.com/warestack/cc/tree/main/class-4)

### 03/11/2026
After drawing my database models on a piece of paper, I think I am ready to create the models for my new tables.
I had to learn how to create related tables with SQLAlchemy.

A few decisions I made:
- Convert all models to use the Declarative Base Class because all documentation now uses this. It is difficult to read and understand the SQLAlchemy docs otherwise.
- Post.body will be `Text` as it may be content of a large size
- Use `func.now()` to get the current UTC time as the default for this function is naive of timezone

Sources:
- [Declarative Base](https://docs.sqlalchemy.org/en/21/orm/declarative_styles.html#orm-explicit-declarative-base)
- [Declare Models](https://docs.sqlalchemy.org/en/21/orm/quickstart.html#declare-models)
- [SQLAlchemy Datatypes](https://docs.sqlalchemy.org/en/21/core/type_basics.html)
- [datetime usage](https://docs.python.org/3/library/datetime.html#examples-of-usage-datetime)

### 03/11/2026
I've added all the other models, and all associations. I did all of the code by looking at the documentation for relationships. I still had errors as I couldn't get the back_populates correct for some reason. I used Claude to help me debug the errors and help with the back_populates settings on the models with associations.

Sources:
- [Association Object](https://docs.sqlalchemy.org/en/21/orm/basic_relationships.html#association-object)

### 06/11/2026
- After some time of trial, error and research, I realise that the validation should occur on the type, so my topics now uses a `Literal` list of topics and I check that the list is not empty.
- I will be using the `FutureDatetime` type from `datetime` for expires_at in my schema as per Pydantic docs.
- I've moved `created_at` to the `Base` class of my model so every table will get this field created.
- Added a seed function to seed topics into the db if they don't exist

Sources:
- [datetime Type docs](https://pydantic.dev/docs/validation/2.0/usage/types/datetime/)

### 07/11/2026
- Returning the topics in a post response returns a Topic object. This needs to change to just the topic names.
- Removed status from Post as this will be calculated on demand and not saved to the database

## TODO
- [ ] Update packages to latest version
- [ ] Update README with tech stack
- [ ] Remove placeholder files
- [ ] Update records in tests to assert deactivated user
- [ ] Return topic names instead of topic objects in the PostResponse