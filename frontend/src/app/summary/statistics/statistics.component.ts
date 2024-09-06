import { Component, EventEmitter, Input, Output, signal } from '@angular/core';
import { Router } from '@angular/router';
import { Loader } from '@googlemaps/js-api-loader';
import moment from 'moment';

interface Data {
  total_gain: number;
  total_cost: number
  total_distance: number;
  total_money: number;
  total_rides: number;
  total_time: number;
  top_rides: string[][];
  longest_ride: {start_place: string, end_place: string, distance: number};
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
  @Output() seasonChange = new EventEmitter<{name: string, startValue: number, endValue: number}>();



  constructor(private router: Router) {}
  dates: Date[] | undefined;


  seasons: {name: string, startValue: number, endValue: number}[] = []


  ngOnInit() {
    const cookie = localStorage.getItem('cookie');
    if(cookie === null) {
      this.router.navigate(['/login']);
    }

    for(let name = new Date().getFullYear(); name >= 2022; name--) {
      let startValue = new Date(`${name}/01/01 00:00:01`).getTime()/1000;
      let endValue = new Date(`${name}/12/31 23:59:59`).getTime()/1000;
    this.seasons.push({name: `${name}`, startValue, endValue});
    
  }
  }
  formatDate(date: number) {
    return moment.unix(date).format('DD.MM.YYYY');
  }




  openModal() {
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage') as HTMLImageElement;
    modal.style.display = 'block';
    modalImg.src = this.data.map;
  }

  closeModal(event: MouseEvent) {
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage') as HTMLImageElement;
    if (event.target === modal || event.target === modalImg) {
      modal.style.display = 'none';
    }
  }

  
  selectSeason(season: {name: string, startValue: number, endValue: number}) {
    console.log('Selected season:', season.startValue, season.endValue);
    this.seasonChange.emit(season);
  }

  

}