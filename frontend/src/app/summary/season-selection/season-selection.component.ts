import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-season-selection',
  templateUrl: './season-selection.component.html',
  styleUrls: ['./season-selection.component.css']
})
export class SeasonSelectionComponent {
  @Output() seasonChange = new EventEmitter<number>();


  constructor(private router: Router) {};


  seasons: {name: number, value: number}[] = []
  ngOnInit() {
    for(let name = new Date().getFullYear(); name >= 2022; name--) {
      let value = new Date(`${name}/01/01 11:24:00`).getTime()
    this.seasons.push({name, value});
  }

}


  selectSeason(season: number) {
    console.log('Selected season:', season);
    this.seasonChange.emit(season);
  }
}