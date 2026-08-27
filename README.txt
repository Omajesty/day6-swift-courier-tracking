# Swift Arrow Couriers — Tracking Window

Swift Arrow Couriers is a small command-line parcel tracking system.

It allows authorized staff to:

* Sign in securely.
* Get information about a parcel.
* Add new parcels.
* Update parcel information.
* Delete parcels.
* Search parcels by tracking code, city, or status.
* Cache recent results so repeated searches can be faster.
* Protect passwords and important files using hashing.
* Use JWT tokens to authenticate requests.

## Getting Started

### Requirements

You need Python installed on your computer.

You can check whether Python is installed by running:

```bash
python --version
```

### Start the application

From the project folder, run:

```bash
python main.py
```

The application will start and allow you to sign in.

## Signing In

After signing in successfully, the system gives you a JWT authentication token.

A JWT usually looks like this:

```text
xxxxx.yyyyy.zzzzz
```

The three sections are separated by two dots (`.`).

You need to include this token when making requests.

For example:

```text
<your-jwt> GET parcel SA-1998500-IY
```

The system checks the token before allowing you to access protected parcel information.

When a token is invalid or has expired, the request is rejected with an authentication error such as:

```text
401 Unauthorized
```

When you are finished, use the application's sign-out option. A valid session should not be reused after signing out.

## Working With Parcels

The tracking system uses simple commands built around HTTP-style verbs.

For example:

```text
<your-jwt> GET parcel SA-1998500-IY
```

This means:

> "Using my authentication token, get the parcel with tracking code `SA-1998500-IY`."

The main operations are:

| Command  | Purpose                     |
| -------- | --------------------------- |
| `GET`    | Retrieve parcel information |
| `POST`   | Add a new parcel            |
| `PUT`    | Update an existing parcel   |
| `DELETE` | Remove a parcel             |

The exact format of the data required by `POST`, `PUT`, and `DELETE` depends on how the application handles those requests.

## How a Tracking Request Works

When you enter:

```text
<your-jwt> GET parcel SA-1998500-IY
```

the request passes through several parts of the application.

### 1. The request is read

`handlers.py` receives the command and works out what the user is asking the system to do.

### 2. The JWT is checked

`auth.py` checks whether the authentication token is valid.

`tokens.py` reads the JWT and verifies its signature and expiration time.

If the token has been changed, forged, or has expired, access is denied.

### 3. The parcel is searched

`lookups.py` handles the request to find the parcel.

The system can use the indexes in `indexes.py` to locate the requested parcel efficiently.

### 4. The cache is checked

Before performing a full search, `cache.py` can check whether the requested result was recently retrieved.

If the answer is already cached, the application can return it without repeating the same lookup.

### 5. The result is displayed

Finally, `main.py` receives the result and prints it to the user.

## Project Structure

Each Python file has a specific responsibility.

### `main.py`

The entry point of the application.

It:

* Starts the program.
* Reads user input.
* Sends commands to the appropriate modules.
* Displays results and errors.

Start the application with:

```bash
python main.py
```

### `handlers.py`

Understands the command entered by the user.

For example, it can recognize:

```text
GET parcel SA-1998500-IY
```

and determine that this is a request to retrieve a parcel.

### `auth.py`

Handles user authentication.

It is responsible for things such as:

* Signing users in.
* Checking authentication tokens.
* Signing users out.

### `tokens.py`

Handles JWT authentication tokens.

A JWT contains three main parts:

```text
header.payload.signature
```

The signature helps the application detect whether someone has modified or forged the token.

Tokens can also contain an expiration time. An expired token is rejected.

### `hashing.py`

Contains the hashing and salting functionality.

It is used for protecting passwords and creating hashes used by the application.

Passwords are processed using SHA-256 together with a salt.

The basic operation is:

```text
SHA-256(salt + password)
```

Each user has their own salt, which is stored with the user's information in `staff.json`.

### `cache.py`

Provides a small cache for recently requested results.

The main operations are:

```text
cache_get
cache_put
cache_wipe
```

The cache keeps the last 10 answers so frequently requested information can be retrieved more quickly.

### `store.py`

Contains shared data structures and file locations used by the application.

Other modules use it when they need access to shared storage information.

### `seal.py`

Creates and checks a hash of `parcels.json`.

The hash acts like a digital fingerprint for the parcel data.

If the contents of the file change, its hash should also change.

### `indexes.py`

Maintains lookup indexes for parcel information.

The indexes help the application find parcels using information such as:

* Tracking code
* City
* Status

Instead of checking every parcel every time, the application can use these indexes to locate matching records more efficiently.

### `parcels.py`

Handles the actual parcel data.

It provides functionality for:

* Loading parcels.
* Saving parcels.
* Adding parcels.
* Updating parcels.
* Deleting parcels.

### `format.py`

Controls how parcel information is displayed to the user.

Keeping formatting in a separate module means the application's data-handling code does not have to worry about how the information looks on screen.

### `lookups.py`

Handles `GET` operations.

For example:

```text
GET parcel SA-1998500-IY
```

This module finds and returns the requested parcel information.

### `writes.py`

Handles operations that change parcel data.

It is responsible for:

```text
POST
PUT
DELETE
```

These operations allow the application to create, modify, and remove parcel records.

## Security

The project uses several security mechanisms.

### Password hashing

Passwords should not be stored as plain text.

Instead, the application uses a salt and SHA-256 hashing process:

```text
password + salt
        ↓
     SHA-256
        ↓
   password hash
```

Each staff member has a separate salt.

### JWT authentication

After successful sign-in, the application uses a JWT to identify the authenticated user.

A valid JWT has the structure:

```text
header.payload.signature
```

If someone modifies the token, its signature will no longer match and the application should reject it.

Expired tokens are also rejected.

### Parcel file integrity

`seal.py` generates a hash for `parcels.json`.

This can be used to detect unexpected changes to the parcel data.

## Typical Request Flow

A normal parcel lookup follows this path:

```text
User
  ↓
main.py
  ↓
handlers.py
  ↓
auth.py
  ↓
tokens.py
  ↓
lookups.py
  ↓
cache.py / indexes.py
  ↓
parcels.py
  ↓
format.py
  ↓
main.py
  ↓
User
```

For example:

```text
<your-jwt> GET parcel SA-1998500-IY
```

is processed approximately as follows:

1. `handlers.py` reads the command.
2. `auth.py` checks the JWT.
3. `tokens.py` verifies the token.
4. `lookups.py` handles the parcel search.
5. `cache.py` checks whether the result is already cached.
6. If necessary, `indexes.py` helps locate the parcel.
7. `parcels.py` provides the parcel data.
8. `format.py` prepares the information for display.
9. `main.py` prints the final response.

## Important Files

The most important files to understand first are:

```text
main.py       → Start here
handlers.py   → Understand user commands
auth.py       → Understand authentication
tokens.py     → Understand JWTs
lookups.py    → Understand parcel searches
writes.py     → Understand parcel changes
parcels.py    → Understand parcel storage
```

If you are new to the project, reading these files in that order will give you a good overview of how the application works.

## Data Files

The application uses files such as:

```text
staff.json
parcels.json
```

`staff.json` contains staff authentication information, including the data needed for password verification.

`parcels.json` contains the parcel records used by the tracking system.

Avoid manually changing these files while the application is running unless you understand how the indexes and file integrity checks work.

## Troubleshooting

### The application does not start

Make sure you are running the command from the project directory:

```bash
python main.py
```

Also verify that Python is installed:

```bash
python --version
```

### I receive `401 Unauthorized`

Your JWT may be:

* Missing.
* Invalid.
* Modified.
* Expired.
* From an invalid authentication session.

Sign in again and use the newly generated token.

### A parcel cannot be found

Check that the tracking code is correct.

For example:

```text
SA-1998500-IY
```

should be entered exactly as required by the application.

## In Short

Swift Arrow Couriers is organized so that each part of the system has one main job:

```text
main.py       → Talks to the user
handlers.py   → Understands commands
auth.py       → Handles authentication
tokens.py     → Handles JWTs
hashing.py    → Protects passwords/data with hashes
cache.py      → Speeds up repeated requests
indexes.py    → Makes searches faster
parcels.py    → Manages parcel data
lookups.py    → Handles GET requests
writes.py     → Handles POST/PUT/DELETE
format.py     → Formats results
store.py      → Provides shared storage information
seal.py       → Checks parcel-file integrity
```

The basic workflow is simple:

```text
Sign in
   ↓
Receive JWT
   ↓
Send authenticated command
   ↓
System verifies JWT
   ↓
System finds or changes parcel data
   ↓
Result is displayed
```

For a quick understanding of the codebase, start with `main.py`, then follow a single `GET parcel ...` request through `handlers.py`, `auth.py`, `tokens.py`, and `lookups.py`.
