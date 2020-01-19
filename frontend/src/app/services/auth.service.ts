import { Injectable, NgZone } from '@angular/core';
import { AngularFireAuth } from '@angular/fire/auth';
import { AngularFirestore, AngularFirestoreDocument } from '@angular/fire/firestore';
import { Router } from '@angular/router';
import { PopupService } from './popup.service';
import {User} from '../interfaces/user';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  userData: any; // Save logged in user data

  constructor(
    public afs: AngularFirestore,   // Inject Firestore service
    public afAuth: AngularFireAuth, // Inject Firebase auth service
    public router: Router,
    public ngZone: NgZone, // NgZone service to remove outside scope warning
    public popup: PopupService,
  ) {
    /* Saving user data in localstorage when
    logged in and setting up null when logged out */
    this.afAuth.authState.subscribe(user => {
      if (user) {
        this.userData = user;
        localStorage.setItem('user', JSON.stringify(this.userData));
      } else {
        localStorage.setItem('user', null);
        console.warn('FORCED LOG OUT');
      }
    });
  }

  login(email: string, password: string): Promise<any> {
    return this.afAuth.auth.signInWithEmailAndPassword(email, password)
      .then((result) => {
        this.ngZone.run(() => {
          this.router.navigate(['/app']);
        });
        // this.SetUserData(result.user); //TODO: check if useful
        window.dispatchEvent(new CustomEvent('user:login'));
      }).catch(error => this.popup.error(error.message));
  }

  // Sign up with email/password
  signUp(email, password, username): Promise<any>  {
    return this.afAuth.auth.createUserWithEmailAndPassword(email, password)
      .then((result) => {
        /* Call the SendVerificationMail() function when new user sign
        up and returns promise */
        this.sendVerificationMail();
        this.setUserName(result.user, username);
        window.dispatchEvent(new CustomEvent('user:signup'));
      }).catch(error => this.popup.error(error.message));
  }

  // Send email verification when new user sign up
  sendVerificationMail() {
    return this.afAuth.auth.currentUser.sendEmailVerification()
      .then(() => {
        this.popup.info('Un mail de vérification a été envoyé à votre adresse').then(() => {
            this.router.navigate(['/app']);
          });
      });
  }

  userDetails() {
    return JSON.parse(localStorage.getItem('user'));
  }

  // Reset Forgot password
  forgotPassword(passwordResetEmail) {
    return this.afAuth.auth.sendPasswordResetEmail(passwordResetEmail)
      .then(() => this.popup.info('Password reset email sent, check your inbox.'))
      .catch(error => this.popup.error(error.message));
  }

  // Returns true when user is logged in and email is verified
  isLoggedIn(): boolean {
    const user = JSON.parse(localStorage.getItem('user'));
    return (user !== null && user.emailVerified !== false);
  }

  setUserName(user, username) {
    const userRef: AngularFirestoreDocument<any> = this.afs.doc(`users/${user.uid}`);
    return userRef.set({
      username: username
    }, { merge: true });
  }

  /* Setting up user data when sign in and sign up with username/password,
   in Firestore database using AngularFirestore + AngularFirestoreDocument service */
  SetUserData(user) {
    const userRef: AngularFirestoreDocument<any> = this.afs.doc(`users/${user.uid}`);
    const userData: User = {
      uid: user.uid,
      username: user.username,
      permissions: user.permissions,
      email: user.email,
      displayName: user.displayName,
      photoURL: user.photoURL,
      emailVerified: user.emailVerified
    };
    return userRef.set(userData, {
      merge: true
    });
  }

  // Sign out
  logout(): Promise<any> {
    return this.afAuth.auth.signOut().then(() => {
      localStorage.removeItem('user');
      window.dispatchEvent(new CustomEvent('user:logout'));
    });
  }

}
