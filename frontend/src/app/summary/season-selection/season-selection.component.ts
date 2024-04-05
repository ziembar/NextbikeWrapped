import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-season-selection',
  templateUrl: './season-selection.component.html',
  styleUrls: ['./season-selection.component.css']
})
export class SeasonSelectionComponent {
  @Input() season = new EventEmitter<string>();


  constructor(private router: Router) {};


  setSeason() {
    this.season.emit('2021');
  }
}