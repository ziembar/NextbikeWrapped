import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { env } from 'node:process';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = process.env['API_URL'] || 'http://127.0.0.1:5000/api';

  constructor(private http: HttpClient) {}

  login(number: string, pin: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/api/login`, {"phone": number, "pin": pin });
  }

  getData(start: any, end: any, cookie: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/api/summary`, {start, end, cookie });
  }
}