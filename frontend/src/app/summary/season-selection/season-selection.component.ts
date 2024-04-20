import { Component, EventEmitter, Output } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-season-selection',
  templateUrl: './season-selection.component.html',
  styleUrls: ['./season-selection.component.css']
})
export class SeasonSelectionComponent {
  @Output() seasonChange = new EventEmitter<{name: string, startValue: number, endValue: number}>();



  constructor(private router: Router) {};

  dates: Date[] | undefined;


  seasons: {name: string, startValue: number, endValue: number}[] = []
  ngOnInit() {
    for(let name = new Date().getFullYear(); name >= 2022; name--) {
      let startValue = new Date(`${name}/01/01 00:00:01`).getTime()/1000;
      let endValue = new Date(`${name}/12/31 23:59:59`).getTime()/1000;
    this.seasons.push({name: `${name}`, startValue, endValue});
  }

}


  selectSeason(season: {name: string, startValue: number, endValue: number}) {
    console.log('Selected season:', season.startValue, season.endValue);
    this.seasonChange.emit(season);
  }

  // TODO: fix date selector (probably calibrate UTC time to local time)

}