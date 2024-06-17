FastAPI (Alembic & SQLAlchemy): Detecting all the custom apps automatically.
Source: [Aashir Shakya](https://medium.com/@aashirshakya/fastapi-alembic-sqlalchemy-detecting-all-the-custom-apps-automatically-2936f47f62fa)


Fast API has been a hot topic for all the developer out there since few years. Those who are familiar with Django might find it tedious to manage some stuff by themselves which are already out of the box on Django. One of the troublesome thing in fast API is it does not have it’s own built in mechanism for managing migrations. We need to integrate alembic on our fast api project and tweak its .ini and env file which appears after initializing alembic. Those who are new to fast api might not understand what i am blaberring about but don’t worry i am here to help you through this confusing journey.

Here’s the requirement.

    python ≥ 3.6
    fastapi==0.95.1
    uvicorn==0.22.0
    SQLAlchemy==2.0.12
    psycopg2==2.9.6
    alembic==1.10.4

Structure of the directory

```sh
├── apps
│   ├── users
│   │   ├── __init__.py
│   │   ├── models.py
│   ├── database.py
│   └── __init__.py
├── alembic
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       └── 66d8a54cd297_initial_tables.py
├── config
│   ├── settings.py
├── alembic.ini
```

Let’s start the actual coding.

```sh
# Create a project and initialize a virtual-environment
python3 -m venv env

# Activate the virtual-environment.
source env/bin/activate

# Install required packages.
pip install fastapi uvicorn SQLAlchemy alembic psycopg2


```

3. Create main file which is used for executing the fastapi app.

# main.py

```python
from fastapi import FastAPI

app = FastAPI()
```
4. Create an apps folder which will contain all our application modules. Inside apps create the database.py file which will contain the configurations related to database. For this example i will be using PostgreSQL database but feel free to use any other database you prefer.

```python
# apps/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database Url to connect to.
# recommend to create an environment variable and read the url from it.
DATABASE_URL = "postgresql://<username>:<password>@<host>:<port>/<db>" 

# For mysql: mysql://<username>:<password>@<host>:<port>/<db>

# engine object that connects to the database specified.
engine = create_engine(
    DATABASE_URL # type: ignore
)

# create new session which is bound to the engine object created earlier.
# autocommit and autoflush false means not to make changes in database when there's 
# change in session
Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models which contains necessary functionality to 
# interact with database using ORM.
Base = declarative_base()
```

5. We will be creating the user’s model so create a folder named users inside apps directory. Inside the user folder create a models.py file.

```python
# apps/users/models.py

from sqlalchemy import Column, Integer, String
from apps.database import Base

class User(Base):
    """
      User model which inherits the Base class 
      defined on database.py file.
    """ 
    __tablename__ = "users" # this value will be the name of the table the database.

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String)
    password = Column(String)
```

7. Now we will be initializing alembic on the root folder to keep track of each and every migrations.

 
```sh
alembic init alembic #alembic init <name_of_folder>
```

8. After initializing alembic you will find a folder named alembic.

```sh
├── alembic
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── alembic.ini
```

You can see the alembic folder which appears after executing the above command. It contains folders and file such as:

**Versions**: Folder where all the migrations files of the each modules are stored.

**env.py**: Python script that defines the configuration for migration using alembic. It contains methods and variables such as:

**run_migrations_online**: When we run alembic upgrade command to migrate our changes to database this function is executed.

**run_migrations_offline**: This function helps to generate the migrations as sql script. When we run alembic upgrade head — sql it provides us the sql script depending on the database state as the standard output. It doesn’t apply the migration to database.

We can also add other custom alembic configurations here.

The command also generates alembic.ini file which contains configurations for alembic and logging. You need to define the location of script on alembic.ini and database url before running the migrations.

```sh
[alembic]
# path to migration scripts
script_location = alembic

sqlalchemy.url = "postgresql://<username>:<password>@<host>:<port>/<db>"
```

9. Now lets try to run the migration.

```sh
alembic revision --autogenerate -m "create-user-model"
```

You are welcomed with an error stating:

```sh
FAILED: Can't proceed with - autogenerate option; environment script /<path>/alembic/env.py does
not provide a MetaData object or sequence of objects to the context.
```

To solve this problem you just need to change your alembic env.py file. As you scroll down the env file you can notice that target_metadata is set to None.

```python
# alembic/env.py
from apps.database import Base

target_metadata = None #old

target_metadata = Base.metadata #new
```

**target_metadata** on env.py file is used to refer to the MetaData object which helps to represent the initial state of the database schema. It also contains information about tables, indexes, columns. It’s important because it tells alembic to use this metadata object to generate the migration script. This helps to certify that the base model class used on our models and migration scripts generated are from the same metadata object.

Now lets try to migrate again.

```sh
alembic revision --autogenerate -m "create-user-model"
```

There no any error!. You will receive these standard outputs on your terminal after successful migrations. A table name alembic_version will also be created on your database which keep track of latest migration.

```sh
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
  Generating /home/<user>/<folder_name>/alembic/versions/901e2a9bbf62_create_user_model.py ...  done
```

But wait. Though the migration has been success it did not detect your models. Go and check your migration file which is on alembic/versions folder.

```python
# alembic/versions

"""create user model

Revision ID: 901e2a9bbf62
Revises: 
Create Date: 2023-05-08 10:29:09.699747

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '901e2a9bbf62'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
```

Alembic should have included all your model migration scripts on upgrade for making changes on your database and downgrade for rolling back all your changes. But there’s no any changes. Why is that happening. ?

Well it’s because we need to import our models into the alembic env.py file individually only then will it detect the models.

```python
# alembic/env.py

from apps.users.models import User
```

Now try migrating it again. Before that you need to run your upgrade your alembic script.

```sh
alembic upgrade head

alembic revision --autogenerate -m "create-user-model-revise"

INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'users'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_users_id' on '['id']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_users_username' on '['username']'
  Generating /home/<user>/<folder>/alembic/versions/b20874ca0a0e_create_user_model_revise.py ...  done
```
From the standard output we can conclude that the model user has been detected by alembic finally.

run_migrations_offline, run_migrations_online and target_metadata. Will be discussing about these topics later. We can also add our own configurations related to migrations here.That’s it. We have successfully implemented migrations using alembic.

Although, it works perfectly fine, if you want alembic to detect your models automatically even without importing it individually on alembic env.py file we can tweak our above code slightly.

There are 2 ways to do this:

**Method 1:** 
We will add models class to __init__.py
In the example attached, we add:
```python
# src/models/__init__.py
from .user import User
...
# add more model class bellow this.
```

In env.py: Replace models imported to all 
```python
# Replace 
from src.models import User
# to
from src.models import *

...
# add more model class bellow this.
```


**Method 2:** 
Create a folder named config and add a settings.py file on it.

```python
#config/settings.py

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


PROJECT_ROOT = "apps"

MODEL_FILE_NAME = "models.py"

#add all your app modules here.
INSTALLED_APPS = [
    "apps.users"
]
```
Inside your apps directory create an __init__.py file.

```python
from config.settings import INSTALLED_APPS, MODEL_FILE_NAME
import importlib

for app in INSTALLED_APPS:
    try:
        importlib.import_module(f'{app}.{MODEL_FILE_NAME[:-3]}') # Dynamic imports
    except ModuleNotFoundError as e:
        print(e)
        continue
```

Since i have added the above code on __init__.py file thus it gets invoked whenever the package or module inside it is imported. And as you know we have already imported database.py which is inside an apps module. So when the above code get executed it dynamically import modules which are defined on settings.py INSTALLED_APPS.

Thats pretty much it. Now you won’t need to individually import every single modules on env.py file. You can test it by removing the model imports from env.py file then add some filed on your models. Finally try migrating it.

```sh
alembic upgrade head
alembic revision --autogenerate -m "update-user-model"
```