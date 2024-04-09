import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';

import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { ApiService } from './services/api.service';
import { SummaryComponent } from './summary/summary.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ButtonModule } from 'primeng/button';
import { InputNumberModule } from 'primeng/inputnumber';
import { PasswordModule } from 'primeng/password';
import { CalendarModule } from 'primeng/calendar';


import { SeasonSelectionComponent } from './summary/season-selection/season-selection.component';
import { StatisticsComponent } from './summary/statistics/statistics.component';


@NgModule({
declarations: [
    LoginComponent,
    SummaryComponent,
    AppComponent,
    SeasonSelectionComponent,
    StatisticsComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    ReactiveFormsModule,
    RouterModule,
    RouterModule.forRoot([
      { path: 'login', component: LoginComponent },
      { path: 'summary', component: SummaryComponent },
      { path: '', redirectTo: '/login', pathMatch: 'full' }
    ]),
    
    FormsModule,
    ButtonModule,
    InputNumberModule,
    PasswordModule,
    CalendarModule


  ],
  providers: [
    ApiService
  ],
  bootstrap: [
    AppComponent
  ],
  exports: [RouterModule, SeasonSelectionComponent, StatisticsComponent]

})
export class AppModule { }