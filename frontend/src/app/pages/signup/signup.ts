import { Component} from '@angular/core';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';
import {AuthService} from '../../services/auth.service';

@Component({
  selector: 'page-signup',
  templateUrl: 'signup.html',
  styleUrls: ['./signup.scss'],
})
export class SignupPage {
  username: string;
  email: string;
  password: string;
  submitted = false;

  constructor(
    public router: Router,
    private auth: AuthService,
  ) {}

  onSignup(form: NgForm) {
    this.submitted = true;

    if (form.valid) {
      this.auth.signUp(this.username, this.password, this.username);
    }
  }
}
