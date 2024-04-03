import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-season-selection',
  templateUrl: './season-selection.component.html',
//   styleUrls: ['./season-selection.component.css']
})
export class SeasonSelectionComponent {
  season: string = '';

  constructor(private router: Router) {}

  selectSeason() {
    // Save selected season in localStorage or pass as parameter
    // Redirect to data display page
    this.router.navigate(['/summary']);
  }
}