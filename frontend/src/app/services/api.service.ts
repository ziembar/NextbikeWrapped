import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://127.0.0.1:5000/api';

  constructor(private http: HttpClient) {}

  login(number: string, pin: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/login`, {"phone": number, "pin": pin });
  }

  getData(start: number, end: number, cookie: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/summary`, {start, end, cookie });
  }
}