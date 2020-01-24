import {Component, OnInit} from '@angular/core';
import { NgForm } from '@angular/forms';
import {ActivatedRoute, Router} from '@angular/router';
import {AuthService} from '../../services/auth.service';
import {NavController} from '@ionic/angular';

@Component({
  selector: 'page-signup',
  templateUrl: 'signup.html',
  styleUrls: ['./signup.scss'],
})
export class SignupPage implements OnInit {
  usernameValue: string;
  emailValue: string;
  passwordValue: string;
  submitted = false;

  constructor(
    public router: Router,
    private auth: AuthService,
    private route: ActivatedRoute,
    public navCtrl: NavController,
  ) {}

  ngOnInit() {
    this.route.queryParams.subscribe(() => {
      if (this.router.getCurrentNavigation().extras.state) {
        this.emailValue = this.router.getCurrentNavigation().extras.state.email;
      }
    });
  }

  onSignup(form: NgForm) {
    this.submitted = true;

    if (form.valid) {
      this.auth.signUp(this.emailValue, this.passwordValue, this.usernameValue);
    }
  }
}
