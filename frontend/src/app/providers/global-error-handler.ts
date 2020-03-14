import { Injectable, ErrorHandler } from '@angular/core';


@Injectable({
  providedIn: 'root'
})
export class GlobalErrorHandler implements ErrorHandler {
  errorHandler: any;

  constructor() {
    window.addEventListener('DOMContentLoaded', () => {
      this.errorHandler = new (window as any).StackdriverErrorReporter();
      this.errorHandler.start({
        key: 'AIzaSyAYon52tg3rmodbRusWF3-czgycGnk3j80',
        projectId: 'badenbattle-a0dec',
      });
    });
  }

  handleError(err: any): void {
    this.errorHandler.report(err);
  }
}
