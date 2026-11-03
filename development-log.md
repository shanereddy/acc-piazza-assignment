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

## TODO
- [ ] Update packages to latest version
- [ ] Update README with tech stack
- [ ] Remove placeholder files
- [ ] Update records in tests to assert deactivated user