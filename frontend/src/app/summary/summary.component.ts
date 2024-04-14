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
      if(cookie) {
        const cookieParts = cookie.split('*');
        if(cookieParts.length === 8) {
          const expiryTime = parseInt(cookieParts[5]);
          const expiryDate = new Date(expiryTime);
          const currentDate = new Date();
          if(currentDate > expiryDate) {
            this.router.navigate(['/login']);
          }
        } else {
          this.router.navigate(['/login']);
        }
      } else {
        this.router.navigate(['/login']);
      }
      // this.data.set({
      //   "top_rides": [
      //     [
      //       [
      //         "Plac Politechniki <---> al. Jana Pawła II - Plac Mirowski",
      //         7
      //       ],
      //       [
      //         "Plac Konstytucji <---> Plac Politechniki",
      //         1
      //       ],
      //       [
      //         "Plac Konstytucji <---> Rondo Jazdy Polskiej",
      //         1
      //       ]
      //     ]
      //   ],
      //   "total_calories": 532,
      //   "total_co2": 264,
      //   "total_distance": [
      //     27125
      //   ],
      //   "total_money": 0,
      //   "total_rides": 12,
      //   "total_time": 107.6
      // })
    }




  setSeason(season: {name: string, startValue: number, endValue: number}) {
    this.season.set(season);
    this.getData(season.startValue, season.endValue);
  }



  getData(start: number, end: number){
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