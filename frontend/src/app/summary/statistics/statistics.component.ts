import { Component, Input, signal } from '@angular/core';
import { Router } from '@angular/router';
import { Loader } from '@googlemaps/js-api-loader';
import moment from 'moment';

interface Data {
  total_calories: number;
  total_co2: number;
  total_distance: number;
  total_money: number;
  total_rides: number;
  total_time: number;
  top_rides: string[][];
  map: string;
  no_data: boolean;
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

    // const loader = new Loader({
    //   apiKey: "YOUR_API_KEY",
    // });

    // loader.load().then(async () => {
    //   const { Map } = await google.maps.importLibrary("maps") as google.maps.MapsLibrary;
    //   let map = new Map(document.getElementById("mapDiv") as HTMLElement, {
    //     center: { lat: -34.397, lng: 150.644 },
    //     zoom: 8,
    //   });
    // });
    
  }

  formatDate(date: number) {
    return moment.unix(date).format('DD.MM.YYYY');
  }
  

}