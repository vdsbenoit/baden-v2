# Setup
1. [Initialize your firebase SDK](https://firebase.google.com/docs/admin/setup#initialize-sdk)
2. Parse your Firebase credentials in a `backend/cred.json`
3. Parse the Firebase project ID in `settings.yml`



# Use



# Testing
WIP: [#13](https://gitlab.com/vdsbenoit/baden/-/issues/13)

[Source](https://firebase.google.com/docs/emulator-suite/connect_and_prototype?authuser=1)

Setup the emulator.
````bash
$ firebase init emulators
````
Don't set up a default project.
Init the Firestore emulator

Start the emulator
````bash
$ firebase emulators:start --only firestore
````
