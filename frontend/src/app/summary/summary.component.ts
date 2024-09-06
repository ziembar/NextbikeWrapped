import { Component, OnInit, signal } from '@angular/core';
import { ApiService } from '../services/api.service';
import { Router } from '@angular/router';
import { MessageService } from 'primeng/api';


@Component({
  selector: 'app-summary',
  templateUrl: 'summary.component.html',
  styleUrls: ['summary.component.css'],
  providers: [MessageService]
})
export class SummaryComponent {
  
    constructor(private apiService: ApiService, private router: Router, private toast: MessageService) {}
    data = signal(undefined);
    season = signal({name: undefined, startValue: undefined, endValue: undefined});
    loading = signal(false);
    name = localStorage.getItem('name');

    ngOnInit() {
      const cookie = localStorage.getItem('cookie');
      const exp = localStorage.getItem('exp');

        if(exp && cookie) {
          console.log(Date.now(), parseInt(exp));
          if(Date.now()/1000 > parseInt(exp)) {
              this.router.navigate(['/login']);
          }
        }
        else {
          this.router.navigate(['/login']);
        }
        this.setSeason({name: new Date().getFullYear().toString(), startValue: null, endValue: null});
      }

  setSeason(season: {name: string, startValue: any, endValue: any}) {
    this.season.set(season);
    this.getData(season.startValue, season.endValue);
  }


  back() {
    this.data.set(undefined);
    this.loading.set(false);
  }


  getData(start: any, end: any){
    this.loading.set(true);
    let cookie = '';
    try{
        cookie = localStorage.getItem('cookie');
        if (cookie === null) {
          this.loading.set(false);
          this.toast.add({ severity: 'error', summary: 'Hmm.. spróbuj ponownie się zalogować', detail: 'Token not found' });
          throw 'Token not found';
        }
    }catch(e){
        console.log(e);
        this.loading.set(false);
        this.router.navigate(['/login']);
        return;
    }
    this.apiService.getData(start, end, cookie).subscribe((response: any) => {
      console.log('Data fetched:', response);
      this.data.set(response);
      this.loading.set(false);
    }, error => {
      console.error('Failed to fetch data:', error);
      this.toast.add({life:5000, severity: 'error', summary: 'Ups.. coś poszło nie tak', detail: error.statusText });
      this.loading.set(false);
    });
  }
}