import { Component, signal } from '@angular/core';
import { ApiService } from '../services/api.service';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Validators } from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {


  constructor(private apiService: ApiService, private router: Router, private formBuilder: FormBuilder) {}


  error = signal(false)
  loading = signal(false)

  error_message = 'Wprowadzono niepoprawne dane. Spróbuj ponownie.'


  auth: FormGroup

  ngOnInit() {
    this.auth = this.formBuilder.group({
      phone: [, [Validators.required, Validators.pattern(/^[0-9]{9}$/)]],
      pin: [, [Validators.required, Validators.minLength(5), Validators.maxLength(6)]]
    });
  };





  login() {
    this.loading.set(true)
    const phone = this.auth.get('phone').value
    const pin = this.auth.get('pin').value
    this.apiService.login(phone, pin).subscribe((response: any) => {
      if(response.code !== 200) {
        this.error_message = response.message ?? 'Wprowadzono niepoprawne dane. Spróbuj ponownie.'
        this.error.set(true)
        this.loading.set(false)
        return;
      }
      this.loading.set(false)
      localStorage.setItem('cookie', response.cookie);
      localStorage.setItem('name', response.name);
      this.router.navigate(['/summary']);
    }, error => {
      this.loading.set(false)
      this.error_message = error.statusText ?? 'Wystąpił nieznany błąd. Spróbuj ponownie później.'

      this.error.set(true)
        return;
    });
  }
}

