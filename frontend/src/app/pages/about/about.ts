import { Component } from '@angular/core';

@Component({
  selector: 'page-about',
  templateUrl: 'about.html',
  styleUrls: ['./about.scss'],
})
export class AboutPage {
  date = '25 Avril 2020';
  location = 'Collège St Vincent\nChaussée de Braine, 22\n7060 Soignies';

  constructor() { }

}
