import { Component, Input, signal } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-statistics',
  templateUrl: './statistics.component.html',
  
//   styleUrls: ['./season-selection.component.css']
})



export class StatisticsComponent{


  @Input() data: any[];
  @Input() season: string;
  @Input() name: string;



  constructor(private router: Router) {}

  ngOnInit() {
    const cookie = localStorage.getItem('cookie');
    if(cookie === null) {
      this.router.navigate(['/login']);
    }
  }

}