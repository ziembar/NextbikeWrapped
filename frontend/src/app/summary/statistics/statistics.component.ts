import { Component, Input, signal } from '@angular/core';
import { Router } from '@angular/router';

interface Data {
  total_calories: number;
  total_co2: number;
  total_distance: number[];
  total_money: number;
  total_rides: number;
  total_time: number;
  top_rides: string[][];
}

@Component({
  selector: 'app-statistics',
  templateUrl: './statistics.component.html',
  
  styleUrls: ['./statistics.component.css']
})




export class StatisticsComponent{


  @Input() data: Data;
  @Input() season: {name: undefined, startValue: undefined, endValue: undefined};
  @Input() name: string;



  constructor(private router: Router) {}

  ngOnInit() {
    const cookie = localStorage.getItem('cookie');
    if(cookie === null) {
      this.router.navigate(['/login']);
    }
  }

}