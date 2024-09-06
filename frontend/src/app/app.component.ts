import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { SeasonSelectionComponent } from './summary/season-selection/season-selection.component';
import { StatisticsComponent } from './summary/statistics/statistics.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'

})
export class AppComponent {
  title = 'Nextbike Wrapped';
}


