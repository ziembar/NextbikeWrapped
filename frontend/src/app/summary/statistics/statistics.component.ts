import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Router } from '@angular/router';
import moment from 'moment';

interface Data {
  total_gain: number;
  total_cost: number
  total_distance: number;
  total_money: number;
  total_rides: number;
  total_time: number;
  top_rides: string[][];
  longest_ride: {start_place: string, end_place: string, distance: number, time: number};
  map: string;
  no_data: boolean;
  name: string;
  id: string;
}

@Component({
  selector: 'app-statistics',
  templateUrl: './statistics.component.html',
  
  styleUrls: ['./statistics.component.css']
})




export class StatisticsComponent{


  @Input() data: Data;
  @Input() season: {name: undefined, startValue: undefined, endValue: undefined};
  @Output() seasonChange = new EventEmitter<{name: string, startValue: number, endValue: number}>();



  constructor(private router: Router) {}
  dates: Date[] | undefined;

  formatDate(date: number) {
    return moment.unix(date).format('DD.MM.YYYY');
  }

  goToLogin(){
    this.router.navigate(['/login'])
  }

  floor(num: number) {
    return Math.floor(num);
  }

  isOriginal(){
    try {
      let name1 = localStorage.getItem('name');
      let name2 = this.data.name.toLowerCase()
      return name1.toLowerCase() === name2.toLowerCase()
    } catch {
      return false
    }
    
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
    this.seasonChange.emit(season);
    this.hideCalendar()
  }

  showCalendar() {
    const calendar = document.getElementsByClassName('calendar-modal')[0] as HTMLElement;
    calendar.style.display = 'block';
  }

  hideCalendar() {
    const calendar = document.getElementsByClassName('calendar-modal')[0] as HTMLElement;
    calendar.style.display = 'none';
  }
  

}