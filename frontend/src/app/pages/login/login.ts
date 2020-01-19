import { Component} from '@angular/core';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';
import {AuthService} from '../../services/auth.service';



@Component({
  selector: 'page-login',
  templateUrl: 'login.html',
  styleUrls: ['./login.scss'],
})
export class LoginPage {
  email: string;
  password: string;
  submitted = false;

  constructor(
    public router: Router,
    private auth: AuthService,
  ) { }

  onLogin(form: NgForm) {
    this.submitted = true;

    if (form.valid) {
      this.auth.login(this.email, this.password);
    }
  }

  onSignup() {
    this.router.navigateByUrl('/signup');
  }
}
