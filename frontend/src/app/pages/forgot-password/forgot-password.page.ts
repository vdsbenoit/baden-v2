import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {AuthService} from '../../services/auth.service';
import {NgForm} from '@angular/forms';
import {NavController} from '@ionic/angular';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.page.html',
  styleUrls: ['./forgot-password.page.scss'],
})
export class ForgotPasswordPage implements OnInit {
  emailValue: string;
  submitted = false;

  constructor(
    public router: Router,
    private auth: AuthService,
    private route: ActivatedRoute,
    public navCtrl: NavController,
  ) { }

  ngOnInit() {
    this.route.queryParams.subscribe(() => {
      if (this.router.getCurrentNavigation().extras.state) {
        this.emailValue = this.router.getCurrentNavigation().extras.state.email;
      }
    });
  }

  sentEmail(form: NgForm) {
    this.submitted = true;

    if (form.valid) {
      this.auth.forgotPassword(this.emailValue);
    }
  }

}
