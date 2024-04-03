import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';

import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { ApiService } from './services/api.service';
import { SummaryComponent } from './summary/summary.component';
import { ReactiveFormsModule } from '@angular/forms';
import { SeasonSelectionComponent } from './season-selection/season-selection.component';

@NgModule({
declarations: [
    LoginComponent,
    SeasonSelectionComponent,
    SummaryComponent,
    AppComponent
],
  imports: [
    BrowserModule,
    HttpClientModule,
    ReactiveFormsModule,
    RouterModule,
    RouterModule.forRoot([
      { path: 'login', component: LoginComponent },
      { path: 'summary', component: SummaryComponent },
      { path: '', redirectTo: '/login', pathMatch: 'full' }
    ])
    // Other modules
  ],
  providers: [
    ApiService // Add ApiService to providers
  ],
  bootstrap: [
    AppComponent
  ],
  exports: [RouterModule]

})
export class AppModule { }