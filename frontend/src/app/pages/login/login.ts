import { Component} from '@angular/core';
import { NgForm } from '@angular/forms';
import {NavigationExtras, Router} from '@angular/router';
import {AuthService} from '../../services/auth.service';

@Component({
  selector: 'page-login',
  templateUrl: 'login.html',
  styleUrls: ['./login.scss'],
})
export class LoginPage {
  emailValue: string;
  passwordValue: string;
  submitted = false;

  constructor(
    public router: Router,
    private auth: AuthService,
  ) { }

  onLogin(form: NgForm) {
    this.submitted = true;

    if (form.valid) {
      this.auth.login(this.emailValue, this.passwordValue);
    }
  }

  navigateTo(page: string) {
    const navigationExtras: NavigationExtras = {
      state: {
        email: this.emailValue
      }
    };
    this.router.navigate([page], navigationExtras);
  }

}
