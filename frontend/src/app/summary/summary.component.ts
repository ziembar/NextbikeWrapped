import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { Router } from '@angular/router';


@Component({
  selector: 'app-content',
  templateUrl: 'summary.component.html'
})
export class SummaryComponent implements OnInit {
    data: any;
  
    constructor(private apiService: ApiService, private router: Router) {}
  
    ngOnInit() {
      let token = '';
      try{
          token = localStorage.getItem('token');
          if (token === null) throw 'Token not found';
      }catch(e){
          console.log(e);
          this.router.navigate(['/login']);
          return;
      }
      const season = ''; // Retrieve selected season from localStorage or elsewhere
      this.apiService.getData(season, token).subscribe((response: any) => {
        this.data = response.data;
      }, error => {
        console.error('Failed to fetch data:', error);
      });
    }
  }