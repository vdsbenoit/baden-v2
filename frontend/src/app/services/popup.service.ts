import { Injectable } from '@angular/core';
import { AlertController } from '@ionic/angular';

@Injectable({
  providedIn: 'root'
})
export class PopupService {

  constructor(
    public alertController: AlertController
  ) { }

  async error(text: string, title = 'Erreur') {
    const alert = await this.alertController.create({
      header: title,
      message: text,
      buttons: ['OK']
    });

    await alert.present();
  }

  async info(text: string, title?: string) {
    const alert = await this.alertController.create({
      header: title,
      message: text,
      buttons: ['OK']
    });

    await alert.present();
  }

  async confirm(text: string, confirmHandler: any, declineHandler?: any) {
    const alert = await this.alertController.create({
      header: 'Tu confirmes?',
      message: text,
      buttons: [
        {
          text: "Non, annule",
          role: 'cancel',
          cssClass: 'secondary',
          handler: () => {
            console.log('User refused to confirm "' + text + '"');
            declineHandler();
          }
        },
        {
          text: 'Je confirme',
          handler: () => {
            console.log('User confirme "' + text + '"');
            confirmHandler();
          },
        }
      ]
    });

    await alert.present();
  }

  async yesNo(text: string, yesHandler: any, noHandler?: any) {
    const alert = await this.alertController.create({
      header: 'Tu confirmes?',
      message: text,
      buttons: [
        {
          text: 'Non',
          role: 'cancel',
          cssClass: 'secondary',
          handler: () => {
            console.log('User chose "no" to prompt "' + text + '"');
            noHandler();
          }
        },
        {
          text: 'Oui',
          handler: () => {
            console.log('User chose "yes" to prompt "' + text + '"');
            yesHandler();
          },
        }
      ]
    });

    await alert.present();
  }

}
