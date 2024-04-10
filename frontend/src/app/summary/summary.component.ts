import { Component, OnInit, signal } from '@angular/core';
import { ApiService } from '../services/api.service';
import { Router } from '@angular/router';


@Component({
  selector: 'app-summary',
  templateUrl: 'summary.component.html',
  styleUrls: ['summary.component.css']
})
export class SummaryComponent {
  
    constructor(private apiService: ApiService, private router: Router) {}
    data = signal(undefined);
    season = signal({name: undefined, startValue: undefined, endValue: undefined});
    loading = signal(false);



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
      this.loading.set(false);
    });
  }
}