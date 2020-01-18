import { Component } from '@angular/core';

@Component({
  selector: 'page-about',
  templateUrl: 'about.html',
  styleUrls: ['./about.scss'],
})
export class AboutPage {
  date = '2020-04-25';
  location = 'Collège St Vincent\nChaussée de Braine, 22\n7060 Soignies';

  constructor() { }

}
