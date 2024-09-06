import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
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


  login(number: string, pin: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/api/login`, {"phone": number, "pin": pin });
  }

  getData(start: any, end: any, cookie: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/api/summary`, {start, end, cookie });
  }
}