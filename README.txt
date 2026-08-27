Swift Arrow Couriers - Tracking Window

A simple command-line parcel tracking system for Swift Arrow Couriers. Staff can sign in, track parcels, and manage parcel records securely.

How to Run

Make sure Python is installed, then run:

python main.py

Sign in to receive your JWT token. Use the token when making requests:

<your-jwt> GET parcel SA-1998500-IY

A JWT has two dots and looks like this:

xxxxx.yyyyy.zzzzz

Invalid or expired tokens will be rejected.

Main Features

* Staff authentication with JWT
* Secure password hashing and salting
* Parcel tracking and management
* Search by tracking code, city, or status
* Caching of the last 10 results
* Parcel data integrity checking

## Project Files


main.py       - Starts the application and handles input/output
handlers.py   - Reads and processes commands
auth.py       - Handles sign in, authentication, and sign out
tokens.py     - Creates and verifies JWT tokens
hashing.py    - Handles password hashing and salts
cache.py      - Stores the last 10 results
store.py      - Shared data and file locations
seal.py       - Checks the integrity of parcels.json
indexes.py    - Helps find parcels quickly
parcels.py    - Adds, updates, deletes, and saves parcels
format.py     - Formats parcel information
lookups.py    - Handles GET requests
writes.py     - Handles POST, PUT, and DELETE requests


## How a Request Works

For example:


<your-jwt> GET parcel SA-1998500-IY


The request goes through:


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
main.py


In simple terms, the system reads your request, checks that you are authorized, finds the parcel, and displays the result.

Security

Passwords are protected using SHA-256 with a unique salt for each user.

JWTs are used to make sure only authenticated users can access protected operations. Expired or modified tokens are rejected.

The parcel file also has a hash that can be used to detect unexpected changes.

Quick Start

python main.py

Then sign in and use your JWT to make parcel requests.

For example:

<your-jwt> GET parcel SA-1998500-IY
