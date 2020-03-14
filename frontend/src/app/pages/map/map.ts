import {Component} from '@angular/core';
import {AppComponent} from '../../app.component';

@Component({
  selector: 'page-map',
  templateUrl: 'map.html',
  styleUrls: ['./map.scss']
})

export class MapPage {
  public pageTitle = 'Plan';

  constructor(
    private appComponent: AppComponent,
  ) {}

  getTheme() {
    return this.appComponent.dark ? 'dark' : 'light';
  }
}
