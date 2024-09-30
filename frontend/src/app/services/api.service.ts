import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import moment from 'moment';
@Injectable({
  providedIn: 'root'
})
export class ApiService {

  
  private apiUrl = environment.apiUrl;
  

  constructor(private http: HttpClient) {
    if (environment.apiUrl == 'API_URL_PLACEHOLDER' || !environment.apiUrl) {
      this.apiUrl =  'http://localhost:5000';
    }
  }

  formatDate(date: number) {
    return moment.unix(date).format('DD.MM.YYYY');
  }

  resetPin(number: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/api/resetpin`, {"phone": number });
  }

  login(number: string, pin: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/api/login`, {"phone": number, "pin": pin });
  }

  getData(season: any, cookie: string, name: string, id: any): Observable<any> {
    if(id){
      return this.http.post(`${this.apiUrl}/api/summary`, {id });
    }
    else {
      let season_name: string;
      if(season.name === 'custom'){
        season_name = `${this.formatDate(season.startValue)} - ${this.formatDate(season.endValue)}`
      }
      else{
        season_name = season.name
      }
      return this.http.post(`${this.apiUrl}/api/summary`, {"start": season.startValue, "end": season.endValue, "season_name": season_name,  cookie, name });

    }
  }
}