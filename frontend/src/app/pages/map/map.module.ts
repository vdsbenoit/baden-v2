import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';

import { MapPage } from './map';
import { MapPageRoutingModule } from './map-routing.module';
import {NgxIonicImageViewerModule} from 'ngx-ionic-image-viewer';

@NgModule({
  imports: [
    CommonModule,
    IonicModule,
    MapPageRoutingModule,
    NgxIonicImageViewerModule,
  ],
  declarations: [
    MapPage,
  ]
})
export class MapModule { }
