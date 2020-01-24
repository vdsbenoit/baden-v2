import { Injectable, NgZone } from '@angular/core';
import { AngularFireAuth } from '@angular/fire/auth';
import { AngularFirestore, AngularFirestoreDocument } from '@angular/fire/firestore';
import { Router } from '@angular/router';
import { PopupService } from './popup.service';
import {NavController} from '@ionic/angular';
import {User} from '../interfaces/user';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor(
    public afs: AngularFirestore,   // Inject Firestore service
    public afAuth: AngularFireAuth, // Inject Firebase auth service
    public router: Router,
    public ngZone: NgZone, // NgZone service to remove outside scope warning
    public popup: PopupService,
    private navCtrl: NavController,
  ) {
    /* Saving user data in localstorage when
    logged in and setting up null when logged out */
    this.afAuth.authState.subscribe(user => {
      if (user) {
        if (user.emailVerified) {
          const userRef: AngularFirestoreDocument<any> = this.afs.doc(`users/${user.uid}`);
          userRef.get().subscribe((userSnapshot) => {
            if (userSnapshot.exists) {
              const userData = userSnapshot.data();
              if (!userData.emailVerified) {
                userRef.set({emailVerified: true}, {merge: true});
                userData.emailVerified = true;
              }
              localStorage.setItem('user', JSON.stringify(userData));
              window.dispatchEvent(new CustomEvent('user:login'));
            } else {
              console.log("User with the uid " + user.uid + " not found in the DB");
              localStorage.setItem('user', null);
              window.dispatchEvent(new CustomEvent('user:logout'));
            }
          });
        }
      } else {
        localStorage.setItem('user', null);
        window.dispatchEvent(new CustomEvent('user:logout'));
      }
    });
  }

  getUserData() {
    return JSON.parse(localStorage.getItem('user'));
  }

  login(email: string, password: string): Promise<any> {
    return this.afAuth.auth.signInWithEmailAndPassword(email, password)
      .then((result) => {
        // this.ngZone.run(() => {
        //         //   this.router.navigate(['/home']);
        //         // });
        if (result.user.emailVerified) {
          this.navCtrl.navigateBack('/home');
        } else {
          this.popup.error("Valide d'abord ton adresse email");
          this.logout();
        }
      }).catch(error => this.popup.error(error.message));
  }

// Sign up with email/password
  signUp(email, password, username): Promise<any>  {
    return this.afAuth.auth.createUserWithEmailAndPassword(email, password)
      .then((result) => {
        this.createUserInFirestore(result.user, username);
        this.sendVerificationMail();
        this.navCtrl.navigateBack('/login');
      }).catch(error => this.popup.error(error.message));
  }

// Send email verification when new user sign up
  sendVerificationMail() {
    return this.afAuth.auth.currentUser.sendEmailVerification()
      .then(() => {
        this.popup.info('Un mail de vérification a été envoyé sur ton adresse');
      }).catch((error) => {
        // todo: hangle error with stackdriver
        this.popup.error("Un problème est survenu durant l'envoi du mail de vérification");
      });
  }

// Reset Forgot password
  forgotPassword(passwordResetEmail) {
    return this.afAuth.auth.sendPasswordResetEmail(passwordResetEmail)
      .then(() => {
        this.popup.info("On t'a envoyé un email");
      })
      .catch(error => this.popup.error(error.message));
  }

// Returns true when user is logged in and email is verified
  isLoggedIn(): boolean {
    const user = JSON.parse(localStorage.getItem('user'));
    return (user !== null && user.emailVerified !== false);
  }

  setUserName(uid, username) {
    const userRef: AngularFirestoreDocument<any> = this.afs.doc(`users/${uid}`);
    return userRef.set({ username: username }, { merge: true });
  }

  /* Sync user data from FireAuth to Firestore DB.
     Return a promise with the userRef
   */
  createUserInFirestore(user, username) {
    const userRef: AngularFirestoreDocument<any> = this.afs.doc(`users/${user.uid}`);
    const userData: User = {
      uid: user.uid,
      username: username,
      permissions: null,
      email: user.email,
      emailVerified: user.emailVerified,
    };
    return userRef.set(userData, { merge: true })
      .catch(() => {
        console.log("Could not write user data in DB");
        this.popup.error("Impossible d'accéder à la DB utilisateurs. Contacte un administrateur");
      });
  }

// Sign out
  logout(): Promise<any> {
    return this.afAuth.auth.signOut();
  }

}
