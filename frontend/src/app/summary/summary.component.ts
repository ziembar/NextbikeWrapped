import { Component, OnInit, signal } from '@angular/core';
import { ApiService } from '../services/api.service';
import { Router } from '@angular/router';
import { SeasonSelectionComponent } from './season-selection/season-selection.component';
import { StatisticsComponent } from './statistics/statistics.component';


@Component({
  selector: 'app-summary',
  templateUrl: 'summary.component.html',
})
export class SummaryComponent {
  
    constructor(private apiService: ApiService, private router: Router) {}
    season = signal(null) // Retrieve selected season from localStorage or elsewhere
    data: any = [];

    getData(){
      let token = '';
      try{
          token = localStorage.getItem('token');
          if (token === null) throw 'Token not found';
      }catch(e){
          console.log(e);
          this.router.navigate(['/login']);
          return;
      }
      this.apiService.getData(this.season(), token).subscribe((response: any) => {
        this.data = response.data;
      }, error => {
        console.error('Failed to fetch data:', error);
      });
    }
  }