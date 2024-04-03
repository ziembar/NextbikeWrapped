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
import { SeasonSelectionComponent } from './season-selection/season-selection.component';
import { ButtonModule } from 'primeng/button';
import { InputNumberModule } from 'primeng/inputnumber';
import { PasswordModule } from 'primeng/password';

@NgModule({
declarations: [
    LoginComponent,
    SeasonSelectionComponent,
    SummaryComponent,
    AppComponent
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