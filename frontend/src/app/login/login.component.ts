import { Component } from '@angular/core';
import { ApiService } from '../services/api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {


  constructor(private apiService: ApiService, private router: Router) {}

  login(event: Event, phone: string, pin: string) {
    event.preventDefault();
    console.log(event);
    this.apiService.login(phone, pin).subscribe((response: any) => {
      if(response.code !== 200) {
        console.error('Login failed:', response);
        return;
      }
      localStorage.setItem('cookie', response.cookie);
      localStorage.setItem('name', response.name);
      this.router.navigate(['/summary']);
    }, error => {
      console.error('Login failed:', error);
    });
  }
}